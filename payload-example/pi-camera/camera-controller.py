import socket
import cv2
import numpy as np
import struct

SERVER_IP = "192.168.1.158"  # Replace with the Raspberry Pi's IP address
SERVER_PORT = 5050
BUFFER_SIZE = 8192  # Adjust the buffer size based on your requirements

def receive_image():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        img_counter = 0
        while True:
            # Receive image size as a 4-byte integer
            size_data = client_socket.recv(4)
            if not size_data:
                break

            # Convert received size data to integer
            size = struct.unpack(">I", size_data)[0]

            # Receive image data
            data = b""
            while len(data) < size:
                chunk = client_socket.recv(min(size - len(data), BUFFER_SIZE))
                if not chunk:
                    break
                data += chunk

            # Convert received data to image
            try:
                image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)

                # Display the image if it is valid
                if image is not None and image.size != 0:
                    #cv2.imshow("Received Image", image)
                    #cv2.waitKey(1)
                    #save image
                    img_name = "frame_{}.png".format(img_counter)
                    folder = "images/"
                    cv2.imwrite(folder+img_name, image)
                    print("{} written!".format(img_name))

                    img_counter += 1
                else:
                    print("Invalid image received")

            except Exception as e:
                print("Error decoding image:", e)

    except socket.error as e:
        print("Socket error:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    receive_image()
