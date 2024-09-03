import os
import sys
import shutil
import numpy as np
import json
import subprocess
import fnmatch
import cv2
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
        for file in files:
            if samples_processed >= num_samples:
                break

            if file.endswith('_img1.png') or file.endswith('_img2.png'):
                file_path = os.path.join(root, file)
                print(f"Displaying sample {samples_processed + 1}: {file_path}")
                add_darkness(file_path)
                samples_processed += 1

        if samples_processed >= num_samples:
            break

    print(f"Displayed {samples_processed} samples")

def clone_directory(src, dst):
    shutil.copytree(src, dst)


def darken_images_in_directory(directory, checkpoint_file, darkness_factor=0.12):
    num_images = 0
    checkpoints = {}

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoints = json.load(f)

    for root, _, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, "*_img1.png") or fnmatch.fnmatch(file, "*_img2.png"):
                file_path = os.path.join(root, file)

                if file_path in checkpoints and checkpoints[file_path] == True:
                    print(f"Skipping already darkened image: {file_path}")
                else:
                    img = Image.open(file_path)
                    img_np = np.array(img)
                    img_dark_np = (img_np * darkness_factor).astype('uint8')
                    img_dark = Image.fromarray(img_dark_np)
                    img_dark.save(file_path)
                    num_images += 1
                    checkpoints[file_path] = True
                    with open(checkpoint_file, 'w') as f:
                        json.dump(checkpoints, f)

    return num_images


if __name__ == '__main__':
    src_dir = "./FlyingChairsOcc/data"
    dst_dir = r"/media/anil/New Volume2/Nihal/Low_Light_dataset/FlyingChairsOcc_dark"
    checkpoint_file = 'darken_images_checkpoints.json'

    # print(f"Listing files in {src_dir}...")
    # list_files_in_directory(src_dir)
    print(f"Displaying samples from {src_dir}...")
    num_samples = 1
    display_sample_images(src_dir, num_samples)

    if num_samples > 0:
        proceed = input("Do you want to proceed with cloning and darkening the dataset? (y/n): ")
        if proceed.lower() != 'y':
            print("Aborted.")
            exit()

    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        print(f"Removed existing directory: {dst_dir}")

    print(f"Cloning directory {src_dir} to {dst_dir}...")
    clone_directory(src_dir, dst_dir)
    print(f"Clone completed.")
    
    print(f"Starting to darken images in {dst_dir}...")
    num_samples_darkened = darken_images_in_directory(dst_dir, checkpoint_file)
    print(f"Darkening completed: {num_samples_darkened} samples darkened")
