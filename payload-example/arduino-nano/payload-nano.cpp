#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main() {
    const char *port = "/dev/ttyACM0";
    int serial_port = open(port, O_RDWR);

    if (serial_port < 0) {
        perror("Error opening serial port");
        return 1;
    }

    // Set serial port settings
    struct termios tty;
    memset(&tty, 0, sizeof(tty));
    if (tcgetattr(serial_port, &tty) != 0) {
        perror("Error getting serial port attributes");
        close(serial_port);
        return 1;
    }

    cfsetospeed(&tty, B115200);
    cfsetispeed(&tty, B115200);

    tty.c_cflag &= ~PARENB; // No parity
    tty.c_cflag &= ~CSTOPB; // One stop bit
    tty.c_cflag &= ~CSIZE;  // Clear character size mask
    tty.c_cflag |= CS8;     // 8 data bits
    tty.c_cflag &= ~CRTSCTS; // No hardware flow control
    tty.c_cflag |= CREAD | CLOCAL; // Enable reading and ignore modem control lines

    // Set input mode (non-canonical, no echo, ...)
    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    // Set output mode (raw output)
    tty.c_oflag &= ~OPOST;

    // Apply settings
    if (tcsetattr(serial_port, TCSANOW, &tty) != 0) {
        perror("Error setting serial port attributes");
        close(serial_port);
        return 1;
    }

    // Write a specific byte to the serial port
    unsigned char byte_to_write = 0x01;
    while(byte_to_write < 0x08){
        ssize_t bytes_written = write(serial_port, &byte_to_write, 1);

        if (bytes_written < 0) {
            perror("Error writing to serial port");
        } else {
            printf("Successfully wrote %zd bytes to %s\n", bytes_written, port);
        }
        byte_to_write++;
    }
    // Close the serial port
    close(serial_port);

    return 0;
}
