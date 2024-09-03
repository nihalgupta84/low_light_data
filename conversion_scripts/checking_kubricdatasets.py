import os
from PIL import Image
import flowpy
import matplotlib.pyplot as plt
import numpy as np

def main():
    base_path = "kubricflow/training"
    scene = "scene_4371"

    # Read images using PIL
    image_folder = os.path.join(base_path, "images", scene)
    image_files = [f"frame_0{i}.png" for i in range(1, 4)]
    images = [Image.open(os.path.join(image_folder, img_file)) for img_file in image_files]

    # Read forward flow using flowpy
    forward_flow_folder = os.path.join(base_path, "forward_flow", scene)
    forward_flow_file = "frame_01.flo"
    forward_flow = flowpy.flow_read(os.path.join(forward_flow_folder, forward_flow_file))

    # Read backward flow using flowpy
    backward_flow_folder = os.path.join(base_path, "backward_flow", scene)
    backward_flow_file = "frame_01.flo"
    backward_flow = flowpy.flow_read(os.path.join(backward_flow_folder, backward_flow_file))

    # Call the function with the loaded images and flow data
    show_images_and_flow(images, forward_flow, backward_flow)

def show_images_and_flow(images, forward_flow, backward_flow):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    for i, img in enumerate(images):
        axes[0, i].imshow(img)
        axes[0, i].axis("off")
        axes[0, i].set_title(f"frame_0{i + 1}.png")

    # Convert optical flow to color map for visualization
    forward_flow_color = flowpy.flow_to_rgb(forward_flow)
    backward_flow_color = flowpy.flow_to_rgb(backward_flow)

    axes[1, 0].imshow(forward_flow_color)
    flowpy.attach_arrows(axes[1, 0], forward_flow_color)
    axes[1, 0].axis("off")
    axes[1, 0].set_title("forward_flow")

    axes[1, 1].imshow(backward_flow_color)
    flowpy.attach_arrows(axes[1, 1], backward_flow_color)
    axes[1, 1].axis("off")
    axes[1, 1].set_title("backward_flow")

    # Remove the unused subplot
    axes[1, 2].axis("off")

    plt.show()

if __name__ == "__main__":
    main()
