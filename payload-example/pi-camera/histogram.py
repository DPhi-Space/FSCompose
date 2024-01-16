import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def process_images_in_folder(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Construct the full path to the image
            image_path = os.path.join(folder_path, filename)

            # Calculate the highest red threshold for the current image
            max_threshold = calculate_highest_red_threshold(image_path)

            # Print the result (you can modify this part based on your requirements)
            print(f"Image: {filename}, Max Red Threshold: {max_threshold}")
            # save this to a file
            with open('red_threshold.txt', 'a') as f:
                f.write(f"Image: {filename}, Max Red Threshold: {max_threshold}\n")


if __name__ == "__main__":
    # Replace 'path/to/your/imgs' with the actual path to your images folder
    imgs_folder_path = 'images/'
    
    process_images_in_folder(imgs_folder_path)
