#include <Wire.h>

#define I2C_ADDRESS 0

#define OPCODE_ALIVE  0x0000
#define OPCODE_LED1   0x00B1
#define OPCODE_LED2   0x00B2
#define OPCODE_LED3   0x00B3
#define OPCODE_LED4   0x00B4

void setup() {
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);

  Wire.begin(I2C_ADDRESS); 
  Wire.onReceive(receiveEvent); 

  Serial.begin(115200);
  Serial.println("MKR Ready to receive commands");
}

void loop() {
}


void receiveEvent(int howMany) {
  if (howMany >= 2) {
    byte input[2];
    input[0] = Wire.read();
    input[1] = Wire.read();
    
    
    unsigned int opCode = (input[0] << 8) | input[1];
    
    
    switch(opCode) {
      case OPCODE_ALIVE:
        Serial.println("I am Alive");
        break;
      case OPCODE_LED1: 
        blink_led(7);
        break;
      case OPCODE_LED2: 
        blink_led(8);
        break;
      case OPCODE_LED3:
        blink_led(9);
        break;
      case OPCODE_LED4:
        blink_led(10);
        break;
      default:
        Serial.println("Unknown command");
        break;
    }
  }
}

void blink_led(int led) {
  Serial.print("Blinking LED ");
  Serial.println(led);
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
}
