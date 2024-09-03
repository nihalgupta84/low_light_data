# import os
# import shutil
# import cv2
#
# input_dir = "./FlyingChairs_release_normal/data"
# output_dir = "./FlyingChairs_release_dark"
#
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)
# print(output_dir)
# converted = 0
#
# for filename in os.listdir(input_dir):
#     file_ext = os.path.splitext(filename)[-1].lower()
#     input_path = os.path.join(input_dir, filename)
#     output_path = os.path.join(output_dir, filename)
#     if file_ext == ".ppm":
#         print(f"Processing {input_path} -> {output_path}")
#         img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
#         cv2.imshow('original image', img)
#         img_dark = cv2.convertScaleAbs(img, alpha=0.04, beta=0)
#         cv2.imshow('dark image', img_dark)
#         cv2.waitKey(0)
#         cv2.imwrite(output_path, img_dark)
#         converted += 1
#     else:
#         shutil.copyfile(input_path, output_path)
#
# print(f"Conversion completed. {converted} samples converted.")


import os
import shutil
import cv2
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

input_dir = "FlyingChairs_release/data"
output_dir = "../ll__datasets/FlyingChairs_release/data"

def process_image(args):
    input_path, output_path = args
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    img_dark = cv2.convertScaleAbs(img, alpha=0.04, beta=0)
    cv2.imwrite(output_path, img_dark)
    return 1

if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [(os.path.join(input_dir, f), os.path.join(output_dir, f))
                   for f in os.listdir(input_dir) if f.lower().endswith('.ppm')]

    non_image_files = [(os.path.join(input_dir, f), os.path.join(output_dir, f))
                       for f in os.listdir(input_dir) if not f.lower().endswith('.ppm')]

    converted = 0
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(tqdm(executor.map(process_image, image_files), total=len(image_files), desc="Converting images"))
        converted = sum(results)

    # Copy non-image files
    for src, dst in non_image_files:
        shutil.copyfile(src, dst)

    print(f"Conversion completed. {converted} samples converted.")


# import os
# import cv2

# input_dir = "./FlyingChairs_release/data"
# output_dir = "./media/anil/New Volume1/Nihal_Low_Light_Datasets/FlyingChairs_release_dark"

# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)


# converted = 0

# for filename in os.listdir(input_dir):
#     if os.path.splitext(filename)[-1].lower() == '.ppm':
#         input_path = os.path.join(input_dir, filename)
#         output_path = os.path.join(output_dir, filename)
#         print(f"Processing {input_path} -> {output_path}")
#         img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
#         img_dark = cv2.convertScaleAbs(img, alpha=0.04, beta=0)
#         cv2.imwrite(output_path, img_dark)
#         converted += 1

# print(f"Conversion completed. {converted} samples converted.")

# # Set the maximum number of samples to show
# max_samples = 5
# samples_shown = 0

# for filename in os.listdir(input_dir):
#     if os.path.splitext(filename)[-1].lower() == '.ppm':
#         input_path = os.path.join(input_dir, filename)
#         output_path = os.path.join(output_dir, filename)
#         img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
#         img_dark = cv2.convertScaleAbs(img, alpha=0.04, beta=0)

#         # Show the original and processed images side by side
#         cv2.imshow("Original", img)
#         cv2.imshow("Dark", img_dark)
#         cv2.waitKey(0)

#         # Save the processed image to the output directory
#         cv2.imwrite(output_path, img_dark)

#         # Check if we have shown enough samples
#         samples_shown += 1
#         if samples_shown >= max_samples:
#             break

# cv2.destroyAllWindows()
