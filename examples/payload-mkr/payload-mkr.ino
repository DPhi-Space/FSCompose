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
  Serial.begin(115200);
  Serial.println("MKR Ready to receive commands");
}

void blink_led(int led);

void loop() {
  if (Serial.available() >= 2) {
    byte input[4];
    for (int i = 0; i < 2; i++) {
      input[i] = Serial.read();
    }
    

    // Decode OpCode and Data
    unsigned int opCode = (input[0] << 8) | input[1];

    // Handle command
    switch(opCode) {
      case OPCODE_ALIVE:
        Serial.print("I am Alive");
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


void blink_led(int led){
  Serial.print("Blinking LED");
  Serial.print(led);
  digitalWrite(led, HIGH);
  delay(100);
  digitalWrite(led, LOW);
}
