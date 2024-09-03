import os
import sys
import shutil
import numpy as np
import json
import subprocess
import fnmatch
import cv2

from PIL import Image

def add_random_haze(image, haze_density=0.2, haze_intensity_range=(0.4, 0.8)):
    img_float = np.float32(image) / 255.0
    haze_map = np.random.uniform(haze_intensity_range[0], haze_intensity_range[1], img_float.shape[:2])
    haze_map = np.repeat(haze_map[:, :, np.newaxis], 3, axis=2)
    hazy_image = img_float * (1 - haze_density * haze_map) + haze_density * haze_map
    hazy_image_uint8 = np.uint8(hazy_image * 255)

    return hazy_image_uint8

def process_images(image_path, darkness_factor=0.12, haze_density=0.2, haze_intensity_range=(0.4, 0.8), apply_darkness=True, apply_haze=True):
    img = Image.open(image_path)
    img_np = np.array(img)

    if apply_darkness:
        img_np = (img_np * darkness_factor).astype('uint8')

    if apply_haze:
        img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        hazy_img = add_random_haze(img_cv2, haze_density, haze_intensity_range)
        img_np = cv2.cvtColor(hazy_img, cv2.COLOR_BGR2RGB)

    processed_img = Image.fromarray(img_np)
    return processed_img

def display_sample_images(directory, num_samples=1, apply_darkness=True, apply_haze=True):
    samples_processed = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if samples_processed >= num_samples:
                break

            if file.endswith('_img1.png') or file.endswith('_img2.png'):
                file_path = os.path.join(root, file)
                print(f"Displaying sample {samples_processed + 1}: {file_path}")
                processed_img = process_images(file_path, apply_darkness=apply_darkness, apply_haze=apply_haze)
                processed_img.show(title='Processed Image')
                samples_processed += 1

        if samples_processed >= num_samples:
            break

    print(f"Displayed {samples_processed} samples")

def clone_directory(src, dst):
    shutil.copytree(src, dst)

def darken_images_in_directory(directory, checkpoint_file, apply_darkness=True, apply_haze=True, darkness_factor=0.12):
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
                    print(f"Skipping already processed image: {file_path}")
                else:
                    processed_img = process_images(file_path, apply_darkness=apply_darkness, apply_haze=apply_haze)
                    processed_img.save(file_path)
                    num_images += 1
                    checkpoints[file_path] = True
                    with open(checkpoint_file, 'w') as f:
                        json.dump(checkpoints, f)

    return num_images

if __name__ == '__main__':
    src_dir = "./FlyingChairsOcc/data"
    dst_dir = r"/media/anil/New Volume/Nihal/Low_Light_dataset/FlyingChairsOcc_dark"
    checkpoint_file = 'darken_images_checkpoints.json'

    print(f"Displaying samples from {src_dir}...")
    num_samples = 1

    # Get user choice
    apply_darkness = input("Do you want to apply darkness? (y/n): ").lower() == 'y'
    apply_haze = input("Do you want to apply haze? (y/n): ").lower() == 'y'

    display_sample_images(src_dir, num_samples, apply_darkness=apply_darkness, apply_haze=apply_haze)

    if num_samples > 0:
        proceed = input("Do you want to proceed with cloning and processing the dataset? (y/n): ")
        if proceed.lower() != 'y':
            print("Aborted.")
            exit()

    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        print(f"Removed existing directory: {dst_dir}")

    print(f"Cloning directory {src_dir} to {dst_dir}...")
    clone_directory(src_dir, dst_dir)
    print(f"Clone completed.")
    
    print(f"Starting to process images in {dst_dir}...")
    num_samples_processed = darken_images_in_directory(dst_dir, checkpoint_file, apply_darkness=apply_darkness, apply_haze=apply_haze)
    print(f"Processing completed: {num_samples_processed} samples processed")
