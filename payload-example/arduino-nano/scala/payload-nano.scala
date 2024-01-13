import com.fazecast.jSerialComm._

object SerialWrite extends App {

  val portName = "/dev/ttyACM0"
  val baudRate = 115200

  val serialPort: SerialPort = SerialPort.getCommPort(portName)
  serialPort.setBaudRate(baudRate)

  if (serialPort.openPort()) {
    val outputStream = serialPort.getOutputStream

    // Write a specific byte to the serial port
    val byteToWrite: Byte = 0x01.toByte
    outputStream.write(byteToWrite)
    def loop(cnt: Int): Unit = {
      if (cnt > 0) {
        outputStream.write(cnt.toByte)
        Thread.sleep(1000)
        loop(cnt - 1)
      }
    }
    loop(8)

    outputStream.close()
    serialPort.closePort()

    println(s"Successfully wrote byte to $portName")
  } else {
    println(s"Error opening port $portName")
  }
}
