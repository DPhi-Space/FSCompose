const int ledPins[] = {2, 3, 4, 5, 6, 7, 8, 9};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);
const int ldrPin = A6;
uint8_t buffer[10];  // Buffer to store incoming data
int bytesRead = 0;    // Number of bytes read
uint8_t cmd = 0;
String msg;
int ldrValue = 0;

enum{
  LED_PATTERN_1 = 0x01,
  LED_PATTERN_2 = 0x02,
  LED_PATTERN_3 = 0x03,
  LED_PATTERN_4 = 0x04,
  LED_PATTERN_5 = 0x05,
  LED_PATTERN_6 = 0x06,
  LED_PATTERN_7 = 0x07,
  READ_LDR = 0x10,
};

void setup() {
  // Set the LED pins as outputs
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
  pattern1();
  pattern2();
  pattern3();
}
           

void loop() { 

  if (Serial.available() > 0) {
      int servo = 0; // for incoming serial data
      int data = 0;
      bytesRead = Serial.readBytes(buffer, 1);  // Read 2 bytes into buffer
      cmd = buffer[0];

      switch(cmd){
        case LED_PATTERN_1:
          pattern1();
          break;

        case LED_PATTERN_2:
          pattern2();
          break;

        case LED_PATTERN_3:
          pattern3();
          break;
        
        case LED_PATTERN_4:
          pattern4();
          break;
        
        case LED_PATTERN_5:
          pattern5();
          break;
        
        case LED_PATTERN_6:
          pattern6();
          break;
        
        case LED_PATTERN_7:
          pattern7();
          break;

        case READ_LDR:
            break;

        default:
          break;
      };
  }  
}



void pattern1(){
 // Pattern 1: Turn on each LED one by one
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], HIGH);
    delay(200);
    digitalWrite(ledPins[i], LOW);
  }
}

void pattern2(){
  // Pattern 2: Turn on all LEDs at once, then turn them off one by one
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], HIGH);
  }
  delay(500);
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], LOW);
    delay(200);
  }
}

void pattern3(){
  // Pattern 3: Turn on LEDs in an alternate pattern
  for (int i = 0; i < numLeds; i += 2) {
    digitalWrite(ledPins[i], HIGH);
  }
  delay(500);
  for (int i = 0; i < numLeds; i += 2) {
    digitalWrite(ledPins[i], LOW);
  }
  for (int i = 1; i < numLeds; i += 2) {
    digitalWrite(ledPins[i], HIGH);
  }
  delay(500);
  for (int i = 1; i < numLeds; i += 2) {
    digitalWrite(ledPins[i], LOW);
  }
}

void pattern4() {
    // Light up from first to last
    for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], HIGH);
        delay(100);
        digitalWrite(ledPins[i], LOW);
    }
    // Light up from last to first
    for (int i = numLeds - 1; i >= 0; i--) {
        digitalWrite(ledPins[i], HIGH);
        delay(100);
        digitalWrite(ledPins[i], LOW);
    }
}

void pattern5() {
    // Turn all LEDs on
    for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], HIGH);
    }
    delay(500);

    // Turn all LEDs off
    for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], LOW);
    }
    delay(500);
}

void pattern6() {
    for (int j = 0; j < numLeds; j++) {
        for (int i = 0; i < numLeds; i++) {
            digitalWrite(ledPins[i], i == j ? HIGH : LOW);
        }
        delay(100);
    }
}

void pattern7() {
    // Turn all LEDs on
    for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], HIGH);
    }
    delay(500);

    // Turn off LEDs one by one
    for (int i = 0; i < numLeds; i++) {
        digitalWrite(ledPins[i], LOW);
        delay(200);
    }
}


