#include <Adafruit_NeoPixel.h>
#include <Wire.h>

// Pin definitions
#define SENSOR_PIN A0    // Analog pin for the LDR
#define LED_PIN    6     // Pin for the NeoPixel
#define LED_COUNT  16    // Number of NeoPixels

// I2C address for this device
#define I2C_ADDRESS 0 

// Create the NeoPixel strip object
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int sensorValue = 0;    // Variable to store the value coming from the sensor
bool isAnimating = false;  // Flag to check if an animation is running

void setup() {
  pinMode(SENSOR_PIN, INPUT);  // Set the sensor pin as an input
  strip.begin();               // Initialize the NeoPixel strip
  strip.show();                // Turn off all pixels to start
  pinMode(LEDR, OUTPUT);
  Serial.begin(9600);

  // Initialize I2C communication
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent);
}

void loop() {
  digitalWrite(LEDR, LOW);
  delay(300);
  digitalWrite(LEDR, HIGH);
  delay(300);

}

void receiveEvent(int numBytes) {
  digitalWrite(LEDG, HIGH);
  while (Wire.available() > 0) {
    char command = Wire.read();
    Serial.println(command);
    handleCommand(command);
  }
  
  digitalWrite(LEDG, LOW);
}

void handleCommand(char command) {
  switch (command) {
    case 0x01:  // Read and send the sensor value
      updateLEDsBasedOnSensor();
      break;

    case 0x02:  // Run color wipe animation
      isAnimating = true;
      colorWipe(strip.Color(0, 255, 0), 50); // Green wipe
      isAnimating = false;
      break;

    case 0x03:  // Run theater chase animation
      isAnimating = true;
      theaterChase(strip.Color(127, 127, 127), 50); // White chase
      isAnimating = false;
      break;

    case 0x04:  // Run rainbow cycle animation
      isAnimating = true;
      rainbow(5);
      isAnimating = false;
      break;

    default:
      // Handle unknown command
      break;
  }
}

void updateLEDsBasedOnSensor() {
  // Read the value from the LDR sensor
  sensorValue = analogRead(SENSOR_PIN);
  Wire.write(sensorValue);
  // Calculate the number of pixels to light up for each stage
  int numGreenPixels = map(sensorValue, 0, 260, 0, LED_COUNT);
  int numYellowPixels = map(sensorValue, 250, 520, 0, LED_COUNT);
  int numOrangePixels = map(sensorValue, 510, 770, 0, LED_COUNT);
  int numRedPixels = map(sensorValue, 760, 1023, 0, LED_COUNT);

  // Set the color pattern based on the sensor value
  for (int i = 0; i < strip.numPixels(); i++) {
    if (i < LED_COUNT - numGreenPixels) {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    if (i < numGreenPixels) {
      strip.setPixelColor(i, strip.Color(0, 255, 0));
    }
    if (i < numYellowPixels) {
      strip.setPixelColor(i, strip.Color(200, 255, 0));
    }
    if (i < numOrangePixels) {
      strip.setPixelColor(i, strip.Color(200, 100, 0));
    }
    if (i < numRedPixels) {
      strip.setPixelColor(i, strip.Color(255, 0, 0));
    }
  }

  // Update the strip with the new settings
  strip.show();
}

// Color wipe animation
void colorWipe(uint32_t color, int wait) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
    strip.show();
    delay(wait);
  }
}

// Theater chase animation
void theaterChase(uint32_t color, int wait) {
  for (int a = 0; a < 10; a++) {
    for (int b = 0; b < 3; b++) {
      strip.clear();
      for (int c = b; c < strip.numPixels(); c += 3) {
        strip.setPixelColor(c, color);
      }
      strip.show();
      delay(wait);
    }
  }
}

// Rainbow cycle animation
void rainbow(int wait) {
  for (long firstPixelHue = 0; firstPixelHue < 5 * 65536; firstPixelHue += 256) {
    strip.rainbow(firstPixelHue);
    strip.show();
    delay(wait);
  }
}
