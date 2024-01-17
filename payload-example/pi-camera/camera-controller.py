import socket
import shutil
import time
import cv2
import numpy as np
import struct
import os
import matplotlib.pyplot as plt

SERVER_IP = "192.168.1.158"  # Replace with the Raspberry Pi's IP address
SERVER_PORT = 5050
BUFFER_SIZE = 8192  # Adjust the buffer size based on your requirements
histogram_counter = 0

def plot_rgb_histogram(image_path, data_folder):
    global histogram_counter
    # Read the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return

    # Split the image into its channels (B, G, R)
    b, g, r = cv2.split(image)

    # Plot histograms
    plt.figure(figsize=(12, 6))

    plt.subplot(131)
    plt.hist(b.flatten(), bins=256, color='blue', alpha=0.7, rwidth=0.8)
    plt.title('Blue Channel Histogram')

    plt.subplot(132)
    plt.hist(g.flatten(), bins=256, color='green', alpha=0.7, rwidth=0.8)
    plt.title('Green Channel Histogram')

    plt.subplot(133)
    plt.hist(r.flatten(), bins=256, color='red', alpha=0.7, rwidth=0.8)
    plt.title('Red Channel Histogram')

    plt.tight_layout()
    # save the plot to a file
    plt.savefig(data_folder + '/histogram.png')
    histogram_counter += 1

def calculate_highest_red_threshold(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Split the image into its channels (B, G, R)
    b, g, r = cv2.split(image)

    # Compute histogram for the red channel
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])

    # Find the threshold with the maximum red intensity
    max_threshold = np.argmax(hist_r)

    return max_threshold

def process_images_in_folder(image_path, data_path):
    max_threshold = 0  # Initialize the maximum red threshold
    max_threshold_image = ""  # Initialize the corresponding image

    # Iterate through all files in the folder
    for filename in os.listdir(image_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Construct the full path to the image
            full_image_path = os.path.join(image_path, filename)

            # Calculate the highest red threshold for the current image
            current_threshold = calculate_highest_red_threshold(full_image_path)

            # Print the result (you can modify this part based on your requirements)
            print(f"Image: {filename}, Current Red Threshold: {current_threshold}")
            
            # Save this to a file
            with open('red_threshold.txt', 'a') as f:
                f.write(f"Image: {filename}, Max Red Threshold: {max_threshold}\n")
            
            if current_threshold > max_threshold:
                max_threshold = current_threshold
                max_threshold_image = full_image_path
            
    # Move the image with the highest red threshold to the data folder
    if max_threshold_image:
        #destination_path = os.path.join(data_path, os.path.basename(max_threshold_image))
        destination_path = data_path + "/frame.png"
        #os.rename(max_threshold_image, destination_path)
        # shutil is used to move the file to another volume inside docker
        shutil.move(max_threshold_image, destination_path)
        print(f"Image with the highest red threshold moved to: {destination_path}")
        plot_rgb_histogram(destination_path, data_path)

    # Move the file to the data folder
    #os.rename('red_threshold.txt', data_path + '/red_threshold.txt')
    shutil.move('red_threshold.txt', data_path + '/red_threshold.txt')
    

def receive_image():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        image_folder = "images/"
        data_folder = "data/"
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
                    cv2.imwrite(image_folder + img_name, image)
                    print("{} written!".format(img_name))

                    img_counter += 1
                else:
                    print("Invalid image received")
                
                # if img counter is 200, process the images
                if img_counter == 400:
                    process_images_in_folder(image_folder, data_folder)
                    # reset the counter
                    img_counter = 0
                    break

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
    # create image folder if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
    # create data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    receive_image()

    while True:
        time.sleep(10)
