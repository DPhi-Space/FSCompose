#include <Adafruit_NeoPixel.h>

// Pin definitions
#define SENSOR_PIN A0    // Analog pin for the LDR
#define LED_PIN    6     // Pin for the NeoPixel
#define LED_COUNT  16    // Number of NeoPixels
#define DELAY      20    // Delay for sensor reading

// Create the NeoPixel strip object
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

int sensorValue = 0;  // Variable to store the value coming from the sensor
bool isAnimating = false;  // Flag to check if an animation is running

void setup() {
  pinMode(SENSOR_PIN, INPUT);  // Set the sensor pin as an input
  strip.begin();               // Initialize the NeoPixel strip
  strip.show();                // Turn off all pixels to start
  Serial1.begin(115200);          // Initialize serial communication
}

void loop() {
  // Check for serial input
  if (Serial1.available() > 0) {
    digitalWrite(LEDG, HIGH);
    char command = Serial1.read();
    handleCommand(command);
    digitalWrite(LEDG, LOW);
  }
  digitalWrite(LEDR, LOW);
  delay(50);
  digitalWrite(LEDR, HIGH);
  delay(50);

  // If not animating, update LEDs based on sensor value
  /*if (!isAnimating) {
    updateLEDsBasedOnSensor();
  }*/
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
      Serial1.println("Unknown command");
      break;
  }
}

void updateLEDsBasedOnSensor() {
  // Read the value from the LDR sensor
  sensorValue = analogRead(SENSOR_PIN);
  Serial1.println(sensorValue);

  // Calculate the number of pixels to light up for each stage
  int numGreenPixels = map(sensorValue, 0, 260, 0, LED_COUNT);
  int numYellowPixels = map(sensorValue, 250, 520, 0, LED_COUNT);
  int numOrangePixels = map(sensorValue, 510, 770, 0, LED_COUNT);
  int numRedPixels = map(sensorValue, 760, 1023, 0, LED_COUNT);

  // Set the color pattern based on the sensor value
  for (int i = 0; i < strip.numPixels(); i++) {
    if (i < LED_COUNT - numGreenPixels){
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
  //delay(DELAY);
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
