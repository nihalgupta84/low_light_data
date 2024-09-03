
import os
import shutil
import cv2

def add_darkness(image_path, output_path, darkness_factor=0.05):
    img = cv2.imread(image_path)
    # cv2.imshow('Original File:', img)
    img_dark = (img * darkness_factor).astype('uint8')
    # cv2.imshow("Dark Image:", img_dark)
    # cv2.waitKey(0)
    cv2.imwrite(output_path, img_dark)

num_samples = 0
def copy_and_darken_images(src, dst):
    global num_samples  # Add this line to fix the error
    for root, dirs, files in os.walk(src):
        dst_root = root.replace(src, dst)
        os.makedirs(dst_root, exist_ok=True)
        
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dst_root, file)
            
            if file in ['im0.png', 'im1.png']:
                add_darkness(src_path, dst_path)
                num_samples += 1
                print(f"Sample {num_samples} converted: {src_path} -> {dst_path}")
            else:
                shutil.copy2(src_path, dst_path)

if __name__ == '__main__':
    src_dir = "./Autoflow"
    dst_dir = r"/media/anil/New Volume3/Nihal/Low_Light_dataset/Autoflow_dark"
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    print(f"Starting conversion from {src_dir} to {dst_dir}...")
    copy_and_darken_images(src_dir, dst_dir)
    print(f"Conversion completed: {num_samples} samples converted")

