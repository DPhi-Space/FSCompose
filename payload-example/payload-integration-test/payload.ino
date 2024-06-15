#define OPCODE_ALIVE  0x0000
#define OPCODE_TEMP   0x00A1


void setup() {
  Serial.begin(9600);
  Serial.println("Ready to receive commands");
}

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
      case OPCODE_ALIVE: // ALIVE
        Serial.println("I am Alive");
        break;
      case OPCODE_TEMP: // GET_TEMP
        sendTemperature();
        break;
      default:
        Serial.println("Unknown command");
        break;
    }
  }
}

void sendTemperature() {
  // Example function to send temperature
  float temperature = 25;
  Serial.print("Current Temperature: ");
  Serial.println(temperature);
}
