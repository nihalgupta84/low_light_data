import argparse
import numpy as np
import cv2
from PIL import Image
import random

# Create an argument parser
parser = argparse.ArgumentParser(description='Apply low-light effects to image pairs')
parser.add_argument('--input_dir', type=str, required=True, help='Directory containing input image pairs')
parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output image pairs')
parser.add_argument('--noise_level_min', type=float, default=0.05, help='Minimum noise level')
parser.add_argument('--noise_level_max', type=float, default=0.2, help='Maximum noise level')
parser.add_argument('--gaussian_std_min', type=float, default=5, help='Minimum Gaussian noise standard deviation')
parser.add_argument('--gaussian_std_max', type=float, default=20, help='Maximum Gaussian noise standard deviation')
parser.add_argument('--illumination_min', type=float, default=0.3, help='Minimum illumination factor')
parser.add_argument('--illumination_max', type=float, default=0.7, help='Maximum illumination factor')
parser.add_argument('--blur_kernel_min', type=int, default=3, help='Minimum blur kernel size')
parser.add_argument('--blur_kernel_max', type=int, default=7, help='Maximum blur kernel size')
parser.add_argument('--contrast_min', type=float, default=1.2, help='Minimum contrast factor')
parser.add_argument('--contrast_max', type=float, default=1.8, help='Maximum contrast factor')
parser.add_argument('--color_min', type=float, default=0.6, help='Minimum color factor')
parser.add_argument('--color_max', type=float, default=1.0, help='Maximum color factor')
parser.add_argument('--gain_min', type=float, default=0.8, help='Minimum gain for white balance')
parser.add_argument('--gain_max', type=float, default=1.2, help='Maximum gain for white balance')

args = parser.parse_args()


def add_shot_noise(image, noise_level):
    if noise_level <= 0:
        return image  # Return the original image if noise_level is 0 or negative
    image = image.astype(np.float32)
    # Ensure noise_level is positive to avoid division by zero
    noisy_image = np.random.poisson(image * max(noise_level, 0.01)) / max(noise_level, 0.01)
    return noisy_image.clip(0, 255).astype(np.uint8)

def add_gaussian_noise(image, mean, std):
    row, col, ch = image.shape
    noise = np.random.normal(mean, std, (row, col, ch))
    noisy_image = image + noise
    return noisy_image.clip(0, 255).astype(np.uint8)


def adjust_illumination(image, illumination_factor): #gamma function
    image = image.astype(np.float32) / 255.0
    adjusted_image = np.power(image, illumination_factor)
    return (adjusted_image * 255).clip(0, 255).astype(np.uint8)

def apply_motion_blur(image, kernel_size):
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    kernel /= kernel_size
    blurred_image = cv2.filter2D(image, -1, kernel)
    return blurred_image

def adjust_contrast_color(image, contrast_factor, color_factor):
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)
    adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV)
    adjusted_image[:, :, 1] = np.clip(adjusted_image[:, :, 1] * color_factor, 0, 255).astype(np.uint8)
    adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_HSV2BGR)
    return adjusted_image

def apply_white_balance(image, red_gain, green_gain, blue_gain):
    image = image.astype(np.float32)
    image[:, :, 0] *= red_gain
    image[:, :, 1] *= green_gain
    image[:, :, 2] *= blue_gain
    return np.clip(image, 0, 255).astype(np.uint8)

def apply_low_light_effects(frame1, frame2):
    noise_level = random.uniform(args.noise_level_min, args.noise_level_max)
    gaussian_std = random.uniform(args.gaussian_std_min, args.gaussian_std_max)
    illumination_factor = random.uniform(args.illumination_min, args.illumination_max)
    blur_kernel_size = random.randint(args.blur_kernel_min, args.blur_kernel_max)
    contrast_factor = random.uniform(args.contrast_min, args.contrast_max)
    color_factor = random.uniform(args.color_min, args.color_max)
    red_gain = random.uniform(args.gain_min, args.gain_max)
    green_gain = random.uniform(args.gain_min, args.gain_max)
    blue_gain = random.uniform(args.gain_min, args.gain_max)
    
    noisy_frame1 = add_shot_noise(frame1, noise_level)
    noisy_frame2 = add_shot_noise(frame2, noise_level)
    
    noisy_frame1 = add_gaussian_noise(noisy_frame1, 0, gaussian_std)
    noisy_frame2 = add_gaussian_noise(noisy_frame2, 0, gaussian_std)
    
    low_light_frame1 = adjust_illumination(noisy_frame1, illumination_factor)
    low_light_frame2 = adjust_illumination(noisy_frame2, illumination_factor)
    
    blurred_frame1 = apply_motion_blur(low_light_frame1, blur_kernel_size)
    blurred_frame2 = apply_motion_blur(low_light_frame2, blur_kernel_size)
    
    adjusted_frame1 = adjust_contrast_color(blurred_frame1, contrast_factor, color_factor)
    adjusted_frame2 = adjust_contrast_color(blurred_frame2, contrast_factor, color_factor)
    
    wb_frame1 = apply_white_balance(adjusted_frame1, red_gain, green_gain, blue_gain)
    wb_frame2 = apply_white_balance(adjusted_frame2, red_gain, green_gain, blue_gain)
    
    return wb_frame1, wb_frame2
