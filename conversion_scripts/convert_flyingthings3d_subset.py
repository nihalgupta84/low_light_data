import os
import sys
import shutil
import numpy as np
import json
import subprocess
from tqdm import tqdm

from PIL import Image

def add_darkness(image_path, darkness_factor=0.12):
    img = Image.open(image_path)
    img_np = np.array(img)
    img_dark_np = (img_np * darkness_factor).astype('uint8')
    img_dark = Image.fromarray(img_dark_np)

    img.show(title='Original Image')
    img_dark.show(title='Dark Image')

def display_sample_images(directory, num_samples=1):
    samples_processed = 0
    for root, _, files in os.walk(directory):
        if not 'image_clean' in root:
            continue

        for file in files:
            if samples_processed >= num_samples:
                break

            file_path = os.path.join(root, file)

            if file_path.endswith('.png'):
                print(f"Displaying sample {samples_processed + 1}: {file_path}")
                add_darkness(file_path)
                samples_processed += 1

        if samples_processed >= num_samples:
            break

    print(f"Displayed {samples_processed} samples")
def clone_directory(src, dst):
    shutil.copytree(src, dst)

# def darken_images_in_directory(directory, checkpoint_file, darkness_factor=0.12):
#     num_images = 0
#     checkpoints = {}

#     if os.path.exists(checkpoint_file):
#         with open(checkpoint_file, 'r') as f:
#             checkpoints = json.load(f)

#     # Get a list of image paths to process
#     image_paths = []
#     for root, _, files in os.walk(directory):
#         if not 'image_clean' in root:
#             continue

#         for file in files:
#             file_path = os.path.join(root, file)
#             if file_path.endswith('.png'):
#                 image_paths.append(file_path)

#     print(f"Total images to process: {len(image_paths)}")

#     # Process images using tqdm for progress bar
#     for file_path in tqdm(image_paths, desc="Darkening images"):
#         rel_file_path = os.path.relpath(file_path, directory)

#         if rel_file_path in checkpoints and checkpoints[rel_file_path] == True:
#             continue
#         else:
#             img = Image.open(file_path)
#             img_np = np.array(img)
#             img_dark_np = (img_np * darkness_factor).astype('uint8')
#             img_dark = Image.fromarray(img_dark_np)
#             img_dark.save(file_path)
#             num_images += 1
#             checkpoints[rel_file_path] = True
#             with open(checkpoint_file, 'w') as f:
#                 json.dump(checkpoints, f)

#     return num_images


def darken_images_in_directory(directory, checkpoint_file, darkness_factor=0.12):
    num_images = 0
    checkpoints = {}

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoints = json.load(f)

    # Get a list of image paths to process
    image_paths = []
    for root, _, files in os.walk(directory):
        if not 'image_clean' in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.png'):
                image_paths.append(file_path)

    print(f"Total images to process: {len(image_paths)}")

    # Process images using tqdm for progress bar
    for file_path in tqdm(image_paths, desc="Darkening images"):
        rel_file_path = os.path.relpath(file_path, directory)

        if rel_file_path in checkpoints and checkpoints[rel_file_path] == True:
            continue
        else:
            try:
                img = Image.open(file_path)
                img_np = np.array(img)
                img_dark_np = (img_np * darkness_factor).astype('uint8')
                img_dark = Image.fromarray(img_dark_np)
                img_dark.save(file_path)
                num_images += 1
                checkpoints[rel_file_path] = True
                with open(checkpoint_file, 'w') as f:
                    json.dump(checkpoints, f)
            except OSError as e:
                print(f"Error processing image {file_path}: {e}")

    return num_images

def is_directory_structure_identical(src, dst):
    for src_root, src_dirs, src_files in os.walk(src):
        dst_root = src_root.replace(src, dst)

        if not os.path.exists(dst_root):
            return False

        dst_dirs, dst_files = [], []
        for _, dirs, files in os.walk(dst_root):
            dst_dirs = dirs
            dst_files = files
            break

        if set(src_dirs) != set(dst_dirs) or set(src_files) != set(dst_files):
            return False

    return True

if __name__ == '__main__':
    src_dir = r"/media/anil/New Volume1/Nihal/data/FlyingThings3D_subset"
    dst_dir = r"/media/anil/New Volume3/Nihal/low_light_datasets/FlyingThings3D_subset"
    checkpoint_file = 'flyingthings3d_subset_checkpoints.json'

    print(f"Displaying samples from {src_dir}...")
    display_sample_images(src_dir)
    proceed = input("Do you want to proceed with cloning and darkening the dataset? (y/n): ")
    if proceed.lower() != 'y':
        print("Aborted.")
        exit()

    if os.path.exists(dst_dir) and is_directory_structure_identical(src_dir, dst_dir):
        print(f"Directory structure already exists in {dst_dir}. Skipping cloning.")
    else:
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
            print(f"Removed existing directory: {dst_dir}")

        print(f"Cloning directory {src_dir} to {dst_dir}...")
        clone_directory(src_dir, dst_dir)
        print(f"Clone completed.")

    print(f"Starting to darken images in {dst_dir}...")
    num_samples = darken_images_in_directory(dst_dir, checkpoint_file)
    print(f"Darkening completed: {num_samples} samples darkened")
