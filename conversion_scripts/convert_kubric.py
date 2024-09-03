import os
import shutil
import numpy as np


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

def darken_images_in_directory(directory, darkness_factor=0.12):
    num_images = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if file_path.endswith('.png'):
                img = Image.open(file_path)
                img_np = np.array(img)
                img_dark_np = (img_np * darkness_factor).astype('uint8')
                img_dark = Image.fromarray(img_dark_np)
                img_dark.save(file_path)
                num_images += 1

    return num_images


if __name__ == '__main__':
    src_dir = "./kubricflow"
    dst_dir = r"/media/anil/New Volume2/Nihal/Low_Light_dataset/kubricflow_dark"

    print(f"Displaying samples from {src_dir}...")
    display_sample_images(src_dir)
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
    num_samples = darken_images_in_directory(dst_dir)
    print(f"Darkening completed: {num_samples} samples darkened")
