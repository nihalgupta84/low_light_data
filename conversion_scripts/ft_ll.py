import os
import cv2
import shutil

# set the path to the original dataset directory
dataset_path = './FlyingThings3D'

# create the directory for the dark images
dark_path = './FlyingThings3D_dark'
if not os.path.exists(dark_path):
    os.mkdir(dark_path)

# define a function to decrease the brightness of an image
def decrease_brightness(img):
    # convert the image to the HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # decrease the value (brightness) channel by 50%
    hsv[:,:,2] = hsv[:,:,2] * 0.06
    # convert the image back to the BGR color space
    dark = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return dark

# loop over the directories containing the images
num_samples = 0
for directory in ['frames_cleanpass', 'frames_finalpass']:
    for subset in ['TRAIN', 'TEST']:
        for camera in ['left', 'right']:
            for root, dirs, files in os.walk(os.path.join(dataset_path, directory, subset)):
                # create the output directory for the current subset and camera
                output_dir = os.path.join(dark_path, directory, subset, camera)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                for file in files:
                    # check if the file is an image file
                    if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.bmp'):
                        # read the image
                        img_path = os.path.join(root, file)
                        img = cv2.imread(img_path)
                        # cv2.imshow('orginal', img)
                        # decrease the brightness
                        dark = decrease_brightness(img)
                        # cv2.imshow('dark image', dark)
                        # cv2.waitKey(0)
                        # write the dark image to the new directory
                        output_path = os.path.join(output_dir, file)
                        cv2.imwrite(output_path, dark)
                        # print the input and output paths
                        print(f"Converted: {img_path} -> {output_path}")
                        num_samples += 1
                    else:
                        # copy the non-image file to the output directory
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(output_dir, file)
                        shutil.copy2(src_path, dst_path)
                        # print the input and output paths
                        print(f"Copied: {src_path} -> {dst_path}")

for directory in ['optical_flow']:
    for subset in ['TRAIN', 'TEST']:
        for flow_type in ['into_future', 'into_past']:
            for camera in ['left', 'right']:
                src_dir = os.path.join(dataset_path, directory, subset, 'x', flow_type, camera)
                dst_dir = os.path.join(dark_path, directory, subset, 'x', flow_type, camera)
                os.makedirs(dst_dir, exist_ok=True)
                for file in os.listdir(src_dir):
                    if file.endswith('.pfm'):
                        src_path = os.path.join(src_dir, file)
                        dst_path = os.path.join(dst_dir, file)
                        shutil.copy2(src_path, dst_path)
                        print(f"Copied optical flow file: {src_path} -> {dst_path}")
                    else:
                        print(f"Ignored non-PFM file: {os.path.join(src_dir, file)}")


print(f"Conversion completed: {num_samples} samples converted")



# import os
# import cv2
# import shutil

# # set the path to the original dataset directory
# dataset_path = './FlyingThings3D'

# # create the directory for the dark images
# dark_path = './FlyingThings3D_dark'
# if not os.path.exists(dark_path):
#     os.mkdir(dark_path)

# # define a function to decrease the brightness of an image
# def decrease_brightness(img):
#     # convert the image to the HSV color space
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     # decrease the value (brightness) channel by 50%
#     hsv[:,:,2] = hsv[:,:,2] * 0.06
#     # convert the image back to the BGR color space
#     dark = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
#     return dark

# # loop over the directories containing the images
# num_samples = 0
# for directory in ['frames_cleanpass', 'frames_finalpass', 'optical_flow']:
#     for subset in ['TRAIN', 'TEST']:
#         for camera in ['left', 'right']:
#             for root, dirs, files in os.walk(os.path.join(dataset_path, directory, subset)):
#                 # create the output directory for the current subset and camera
#                 output_dir = os.path.join(dark_path, directory, subset, camera)
#                 if not os.path.exists(output_dir):
#                     os.makedirs(output_dir)
#                 for file in files:
#                     # check if the file is an image file
#                     if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.bmp'):
#                         # read the image
#                         img_path = os.path.join(root, file)
#                         img = cv2.imread(img_path)
#                         # decrease the brightness
#                         dark = decrease_brightness(img)
#                         # write the dark image to the new directory
#                         output_path = os.path.join(output_dir, file)
#                         cv2.imwrite(output_path, dark)
#                         # print the input and output paths
#                         print(f"Converted: {img_path} -> {output_path}")
#                         num_samples += 1
#                     else:
#                         # copy the non-image file to the output directory
#                         src_path = os.path.join(root, file)
#                         dst_path = os.path.join(output_dir, file)
#                         shutil.copy2(src_path, dst_path)
#                         # print the input and output paths
#                         print(f"Copied: {src_path} -> {dst_path}")
# print(f"Conversion completed: {num_samples} samples converted")



# import os
# import cv2

# # set the path to the original dataset directory
# dataset_path = './FlyingThings3D'

# # create the directory for the dark images
# dark_path = './media/anil/New Volume1/Nihal Low Light Datasets/FlyingThings3D_dark'
# if not os.path.exists(dark_path):
#     os.mkdir(dark_path)

# # create the directory for the sample dark images
# sample_path = os.path.join(dark_path, 'sample')
# if not os.path.exists(sample_path):
#     os.mkdir(sample_path)

# # define a function to decrease the brightness of an image
# def decrease_brightness(img):
#     # convert the image to the HSV color space
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     # decrease the value (brightness) channel by 50%
#     hsv[:,:,2] = hsv[:,:,2] * 0.06
#     # convert the image back to the BGR color space
#     dark = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
#     return dark

# # loop over the directories containing the images
# for directory in ['frames_cleanpass', 'frames_finalpass', 'optical_flow']:
#     for subset in ['TRAIN', 'TEST']:
#         for camera in ['left', 'right']:
#             for root, dirs, files in os.walk(os.path.join(dataset_path, directory, subset)):
#                 for file in files[:2]:
#                     # check if the file is a PNG image file
#                     if file.endswith('.png'):
#                         # read the image
#                         img_path = os.path.join(root, file)
#                         img = cv2.imread(img_path)
#                         # decrease the brightness
#                         dark = decrease_brightness(img)
#                         # write the dark image to the new directory
#                         dark_path = os.path.join(sample_path, directory, subset, os.path.basename(root), camera)
#                         if not os.path.exists(dark_path):
#                             os.makedirs(dark_path)
#                         dark_file = os.path.join(dark_path, file)
#                         cv2.imwrite(dark_file, dark)
#                         # display the original and dark images
#                         cv2.imshow('Original', img)
#                         cv2.imshow('Dark', dark)
#                         cv2.waitKey(0)
#                         cv2.destroyAllWindows()
