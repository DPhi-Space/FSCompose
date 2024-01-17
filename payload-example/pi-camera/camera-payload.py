import socket
import struct
import time
import io
import cv2
import threading
import queue

camera = cv2.VideoCapture(0)

IP_ADDR = "0.0.0.0"
PORT = 5050

def send_image(conn):
    while True:
        rval, image = camera.read()
        if rval == False: 
            print("No image")
        else:
            # Encode image to JPEG format
            _, img_encoded = cv2.imencode('.jpg', image)
            
            # Send image size as a 4-byte integer
            try:
                conn.sendall(struct.pack(">I", len(img_encoded)))
                print("Sent image")
                
                # Send the image data
                conn.sendall(img_encoded)
            except (socket.error, BrokenPipeError):
                # Handle socket error or broken pipe (connection lost)
                print("Connection lost. Reconnecting...")
                break
            
            # Wait for a short time
            time.sleep(0.5)

if __name__ == "__main__":
    if camera.isOpened() == False:
        print("Error opening video stream or file")

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((IP_ADDR, PORT))
    tcp_socket.listen()
    print("Listening on port", PORT)

    while True:
        try:
            conn, addr = tcp_socket.accept()
            print("Connected to", addr)

            # Create a separate thread for sending images
            send_thread = threading.Thread(target=send_image, args=(conn,))
            send_thread.start()

            send_thread.join()
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C)
            break
        except Exception as e:
            print("Error accepting connection:", e)
        finally:
            # Release resources
            if 'conn' in locals() and conn:
                conn.close()

    # Close the main socket and release camera
    tcp_socket.close()
    camera.release()
