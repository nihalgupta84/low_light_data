import os
import cv2
import shutil

# Define the path of the original dataset
input_dir = "./KITTI_2012"

# Define the path of the new dataset
output_dir = "./ll_datasets/KITTI_2012_dark"

# Check if the output directory exists and create it if necessary
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
else:
    print(f"The output directory {output_dir} already exists.")

# Define the relevant subfolders
subfolders = ['training/colored_0', 'training/colored_1', 'training/image_0', 'training/image_1', 'testing/colored_0', 'testing/colored_1', 'testing/image_0', 'testing/image_1']

# Define the brightness reduction factor
brightness_factor = 0.03

num_samples = 0

# Print a message indicating the input and output directories
print(f"Starting conversion from {input_dir} to {output_dir}...")

# Recursively walk through the input directory and process all relevant files
for root, dirs, files in os.walk(input_dir):
    # Check if the current directory is one of the relevant subfolders
    if root.endswith(tuple(subfolders)):
        for file in files:
            # Check if the file is an image file
            if file.endswith('.png'):
                # Get the full path to the input file
                input_path = os.path.join(root, file)
                # Determine the output directory and filename
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                # Make sure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                # Load the image and apply the desired transformation
                img = cv2.imread(input_path)
                # cv2.imshow('Original Image', img)
                img_dark = cv2.addWeighted(img, brightness_factor, img, 0, 0)
                # cv2.imshow('Transformed Image', img_dark)
                # cv2.waitKey(0)
                # Save the transformed image
                cv2.imwrite(output_path, img_dark)
                # Print a message indicating that the sample has been converted
                print(f"Sample converted: {input_path} --> {output_path}")
                num_samples += 1
    else:
        # Copy the entire directory tree to the output directory
        rel_path = os.path.relpath(root, input_dir)
        output_path = os.path.join(output_dir, rel_path)
        os.makedirs(output_path, exist_ok=True)
        for file in files:
            input_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, rel_path, file)
            shutil.copy2(input_path, output_path)

print(f"Conversion completed: {num_samples} samples converted")
