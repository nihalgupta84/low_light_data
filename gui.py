import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading

update_timer = None

last_processed_image = None

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

# def adjust_illumination(image, illumination_factor):
#     adjusted_image = image.astype(np.float32) * illumination_factor
#     return adjusted_image.clip(0, 255).astype(np.uint8)

def adjust_illumination(image, illumination_factor):
    image = image.astype(np.float32) / 255.0
    gamma = 1.0 / illumination_factor
    adjusted_image = np.power(image, gamma)
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


# GUI application with Tkinter
def create_gui_app(frame1):
    window = tk.Tk()
    window.title("Low-Light Effect Tuning")
    window.minsize(1000, 600)

    # Slider frame
    slider_frame = ttk.Frame(window)
    slider_frame.pack(side=tk.LEFT, fill='y', padx=10, pady=10)

    # Image display frame
    image_frame = ttk.Frame(window)
    image_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)

    # Function to update image based on slider values
    def update_image():
        global last_processed_image 
        scale_factor = 0.5
        noise_level = noise_level_slider.get()
        gaussian_std = gaussian_std_slider.get()
        illumination_factor = illumination_slider.get()
        blur_kernel_size = blur_kernel_slider.get()
        contrast_factor = contrast_slider.get()
        color_factor = color_slider.get()
        red_gain = red_gain_slider.get()
        green_gain = green_gain_slider.get()
        blue_gain = blue_gain_slider.get()
        small_frame1 = cv2.resize(frame1, (0, 0), fx=scale_factor, fy=scale_factor)
        # Apply effects

        processed = add_shot_noise(small_frame1, noise_level)
        processed = add_gaussian_noise(processed, 0, gaussian_std)
        processed = adjust_illumination(processed, illumination_factor)
        processed = apply_motion_blur(processed, blur_kernel_size)
        processed = adjust_contrast_color(processed, contrast_factor, color_factor)
        processed = apply_white_balance(processed, red_gain, green_gain, blue_gain)


        # processed = add_shot_noise(frame1, noise_level)
        # processed = add_gaussian_noise(processed, 0, gaussian_std)
        # processed = adjust_illumination(processed, illumination_factor)
        # processed = apply_motion_blur(processed, blur_kernel_size)
        # processed = adjust_contrast_color(processed, contrast_factor, color_factor)
        # processed = apply_white_balance(processed, red_gain, green_gain, blue_gain)

        processed = cv2.resize(processed, (frame1.shape[1], frame1.shape[0]))
        # img = Image.fromarray(cv2.cvtColor(processed_display, cv2.COLOR_BGR2RGB))
        # photo = ImageTk.PhotoImage(image=img)
        # image_label.configure(image=photo)
        # image_label.image = photo

        # Store the processed image in its original resolution for saving
        # last_processed_image = processed

        img = Image.fromarray(processed)
        photo = ImageTk.PhotoImage(image=img)
        image_label.configure(image=photo)
        image_label.image = photo
        last_processed_image = cv2.cvtColor(np.array(processed), cv2.COLOR_RGB2BGR)


    def update_image_with_delay():
        global update_timer
        if update_timer is not None:
            update_timer.cancel()
        update_timer = threading.Timer(0.5, update_image)  # Adjust delay as needed
        update_timer.start()
    # Sliders
    noise_level_slider = tk.Scale(slider_frame, from_=0.01, to=0.5, resolution=0.01, label="Noise Level", orient=tk.HORIZONTAL, command=lambda event: update_image())
    noise_level_slider.pack(fill='x', expand=True)
    gaussian_std_slider = tk.Scale(slider_frame, from_=10, to=30, resolution=0.1, label="Gaussian STD", orient=tk.HORIZONTAL, command=lambda event: update_image())
    gaussian_std_slider.pack(fill='x', expand=True)
    illumination_slider = tk.Scale(slider_frame, from_=0.1, to=1, resolution=0.01, label="Illumination Factor", orient=tk.HORIZONTAL, command=lambda event: update_image())
    illumination_slider.pack(fill='x', expand=True)
    blur_kernel_slider = tk.Scale(slider_frame, from_=5, to=11, resolution=1, label="Blur Kernel Size", orient=tk.HORIZONTAL, command=lambda event: update_image())
    blur_kernel_slider.pack(fill='x', expand=True)
    contrast_slider = tk.Scale(slider_frame, from_=0.8, to=1.2, resolution=0.01, label="Contrast Factor", orient=tk.HORIZONTAL, command=lambda event: update_image())
    contrast_slider.pack(fill='x', expand=True)
    color_slider = tk.Scale(slider_frame, from_=0.4, to=0.8, resolution=0.01, label="Color Factor", orient=tk.HORIZONTAL, command=lambda event: update_image())
    color_slider.pack(fill='x', expand=True)
    red_gain_slider = tk.Scale(slider_frame, from_=0.6, to=1.0, resolution=0.01, label="Red Gain", orient=tk.HORIZONTAL, command=lambda event: update_image())
    red_gain_slider.pack(fill='x', expand=True)
    green_gain_slider = tk.Scale(slider_frame, from_=0.6, to=1.0, resolution=0.01, label="Green Gain", orient=tk.HORIZONTAL, command=lambda event: update_image())
    green_gain_slider.pack(fill='x', expand=True)
    blue_gain_slider = tk.Scale(slider_frame, from_=0.6, to=1.0, resolution=0.01, label="Blue Gain", orient=tk.HORIZONTAL, command=lambda event: update_image())
    blue_gain_slider.pack(fill='x', expand=True)
    
    # noise_level_slider = ttk.Scale(slider_frame, from_=0.01, to=0.5, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # noise_level_slider.pack(fill='x', expand=True)
    # gaussian_std_slider = ttk.Scale(slider_frame, from_=10, to=30, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # gaussian_std_slider.pack(fill='x', expand=True)
    # illumination_slider = ttk.Scale(slider_frame, from_=0.1, to=0.5, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # illumination_slider.pack(fill='x', expand=True)
    # blur_kernel_slider = ttk.Scale(slider_frame, from_=5, to=11, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # blur_kernel_slider.pack(fill='x', expand=True)
    # contrast_slider = ttk.Scale(slider_frame, from_=0.8, to=1.2, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # contrast_slider.pack(fill='x', expand=True)
    # color_slider = ttk.Scale(slider_frame, from_=0.4, to=0.8, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # color_slider.pack(fill='x', expand=True)
    # red_gain_slider = ttk.Scale(slider_frame, from_=0.6, to=1.0, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # red_gain_slider.pack(fill='x', expand=True)
    # green_gain_slider = ttk.Scale(slider_frame, from_=0.6, to=1.0, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # green_gain_slider.pack(fill='x', expand=True)   
    # blue_gain_slider = ttk.Scale(slider_frame, from_=0.6, to=1.0, length=200, orient='horizontal', command=lambda event: update_image_with_delay())
    # blue_gain_slider.pack(fill='x', expand=True)

    # Image label
    image_label = ttk.Label(image_frame)
    image_label.pack(fill='both', expand=True)
    save_button = ttk.Button(slider_frame, text="Save Image and Settings", command=lambda: save_image_and_settings(
    noise_level_slider.get(),
    gaussian_std_slider.get(),
    illumination_slider.get(),
    blur_kernel_slider.get(),
    contrast_slider.get(),
    color_slider.get(),
    red_gain_slider.get(),
    green_gain_slider.get(),
    blue_gain_slider.get()
))
    save_button.pack(fill='x', expand=True, pady=5)
    update_image()  # Initial image update

    window.mainloop()



def save_image_and_settings(noise_level, gaussian_std, illumination_factor, blur_kernel_size, contrast_factor, color_factor, red_gain, green_gain, blue_gain):
    # Define save path
    global image_file_path
    if last_processed_image is None:
        print("No image to save.")
        return

    save_path = "saved_images"
    os.makedirs(save_path, exist_ok=True)
    base_file_name = os.path.splitext(os.path.basename(image_file_path))[0]
    # Save the image
    image_save_path = os.path.join(save_path, f"{base_file_name}_processed.jpg")
    cv2.imwrite(image_save_path, last_processed_image)
    
    # Save the settings
    settings_save_path = os.path.join(save_path, f"{base_file_name}_settings.txt")
    with open(settings_save_path, "w") as file:
        file.write(f"Noise Level: {noise_level}\n")
        file.write(f"Gaussian STD: {gaussian_std}\n")
        file.write(f"Illumination Factor: {illumination_factor}\n")
        file.write(f"Blur Kernel Size: {blur_kernel_size}\n")
        file.write(f"Contrast Factor: {contrast_factor}\n")
        file.write(f"Color Factor: {color_factor}\n")
        file.write(f"Red Gain: {red_gain}\n")
        file.write(f"Green Gain: {green_gain}\n")
        file.write(f"Blue Gain: {blue_gain}\n")

    print(f"Image and settings saved to '{save_path}'")

# Load an image to start with
image_file_path = 'datasets/KITTI_2015/testing/image_2/000164_10.png'  # Store the file path in a global variable

# Load the image as before
try:
    frame1 = cv2.imread(image_file_path)
    if frame1 is None:
        raise IOError("Could not load the image.")
    if len(frame1.shape) == 2:
        # Grayscale image
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_GRAY2RGB)  # Convert grayscale to RGB
    else:
        # BGR color image
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    create_gui_app(frame1)
except IOError as e:
    print(e)

