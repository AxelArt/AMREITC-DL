import os
import numpy as np
from PIL import Image
from tqdm import tqdm
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Convert PCAP files to PNG images")

# Add an argument to specify the size of the input images in pixels
parser.add_argument("-s", "--size", type=int, help="Size of the input images in pixels")

# Add an argument to specify the color mode of the output image (RGB or grayscale)
parser.add_argument("-c", "--color", type=str, help="Color mode of the output image (RGB or L)")

args = parser.parse_args()

# Get the size of the input images in pixels
image_size = args.size

# Get the color mode of the output image
color_mode = args.color
#color_mode = "L"

# Check if the image size is square
if image_size <= 0:
    print("Image size should be greater than zero and square")
    exit()

# Check if the color mode is valid
if color_mode not in ["RGB", "L"]:
    print("Invalid color mode. Please specify 'RGB' or 'L for gray' for grayscale.")
    exit()

# Set the name of the parent folder that contains the folders with pcap files
parent_folder = ""

# Set the name of the folder where to save the output subfolders
result_folder = ""

for folder in os.listdir(parent_folder):
    # Set the name of the folder that contains the pcap files
    folder_name = os.path.join(parent_folder,folder)

    # Check if the current folder is a directory and not a file
    if os.path.isdir(folder_name):
        # Create the output folder if it does not exist
        output_folder = os.path.join(result_folder,folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for file in tqdm(os.listdir(folder_name)):
            if file.endswith(".pcap"):
                # Read the binary data of the pcap file
                with open(os.path.join(folder_name, file), "rb") as f:
                    data = f.read()

                # Get the size of the pcap file in bytes
                file_size = os.path.getsize(os.path.join(folder_name, file))

                # Calculate the size of the image
                data = np.frombuffer(data, np.uint8)
                if color_mode == "L":
                    if file_size < (image_size*image_size) :
                        data = np.pad(data, (0, (image_size*image_size) - file_size), mode='constant', constant_values=(0, 0))
                    data = data[:image_size*image_size] 
                    data = data.reshape(image_size, image_size)
                elif color_mode == "RGB":
                    if file_size < (image_size*image_size*3) :
                        data = np.pad(data, (0, (image_size*image_size*3) - file_size), mode='constant', constant_values=(0, 0))
                    data = data[:image_size*image_size*3] 
                    data = data.reshape(image_size, image_size, 3)
                # Convert the data to a PIL image
                img = Image.fromarray(data, mode=color_mode)

                # Save the image to a PNG file
                img.save(os.path.join(output_folder, file.replace(".pcap", ".png")))

