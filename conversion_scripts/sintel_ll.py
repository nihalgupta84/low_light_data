import os
import shutil
from PIL import Image, ImageEnhance

# Define the path of the original dataset
input_dir = "./Sintel"

# Define the path of the new dataset
output_dir = "./Sintel_dark"

# Check if the output directory exists and create it if necessary
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
else:
    print(f"The output directory {output_dir} already exists.")

# Define the brightness reduction factor
brightness_factor = 0.01

num_samples = 0

# Print a message indicating the input and output directories
print(f"Starting conversion from {input_dir} to {output_dir}...")

# Loop through the input directory and its subdirectories
for dirpath, dirnames, filenames in os.walk(input_dir):
    # Create the output directory structure if necessary
    relpath = os.path.relpath(dirpath, input_dir)
    outdir = os.path.join(output_dir, relpath)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for filename in filenames:
        # Skip files that are not PNG images
        if not filename.endswith(".png"):
            continue

        # Skip files in the flow subdirectory
        if "flow" in dirpath:
            continue

        # Skip files in the invalid subdirectory
        if "invalid" in dirpath:
            continue

        # Define the input and output file paths
        inpath = os.path.join(dirpath, filename)
        outpath = os.path.join(outdir, filename)

        print(f"Processing file: {inpath}")
        # Open the image file
        img = Image.open(inpath)

        # Reduce the brightness of the image
        enhancer = ImageEnhance.Brightness(img)
        img_dark = enhancer.enhance(brightness_factor)

        # Save the darkened image to the output file path
        img_dark.save(outpath)

        # Print a message indicating that the sample has been converted
        print(f"Sample converted: {inpath} --> {outpath}")
        num_samples += 1

print(f"Conversion completed: {num_samples} samples converted")






# import os
# import shutil
# from PIL import Image, ImageEnhance

# # Define the path of the sample image
# # sample_image_path = "./Sintel/training/clean/alley_1/frame_0002.png"

# # Define the brightness reduction factor
# brightness_factor = 0.01

# # Open the sample image
# # img = Image.open(sample_image_path)

# # Display the original image
# # print("Original image:")
# # img.show()

# # Reduce the brightness of the image
# # enhancer = ImageEnhance.Brightness(img)
# # img_dark = enhancer.enhance(brightness_factor)

# # # Display the darkened image
# # print("Darkened image:")
# # img_dark.show()

# # Define the path of the original dataset
# input_dir = "./Sintel"

# # Define the path of the new dataset
# output_dir = "./Sintel_dark"

# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)

# # Copy the entire directory structure from input_dir to output_dir
# shutil.copytree(input_dir, output_dir)

# num_samples = 0

# # Loop through the new dataset and process the image files
# for root, dirs, files in os.walk(output_dir):
#     for filename in files:
#         filepath = os.path.join(root, filename)
#         if filepath.endswith(".png"):
#             # Open the image file
#             img = Image.open(filepath)

#             # Reduce the brightness of the image
#             enhancer = ImageEnhance.Brightness(img)
#             img_dark = enhancer.enhance(brightness_factor)

#             # Save the darkened image to the same file path
#             img_dark.save(filepath)
#             num_samples += 1

# print(f"Conversion completed: {num_samples} samples converted")

