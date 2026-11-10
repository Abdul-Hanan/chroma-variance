import cv2
import numpy as np
import os

def generate_synthetic_image(width=300, height=300):
    """
    Generates a synthetic color image with distinct color regions
    to demonstrate color divergence.

    The image will have:
    - Top-left: Pure Red (low B, G; high R)
    - Top-right: Pure Green (low B, R; high G)
    - Bottom-left: Pure Blue (high B; low G, R)
    - Bottom-right: Pure White (all channels high)
    - Center circle: Medium Gray (all channels mid-range)

    This setup ensures areas with high and low channel divergence are present.
    """
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Top-left quadrant: Pure Red (BGR: 0, 0, 255)
    # Expected divergence: |0-0| + |0-255| + |255-0| = 0 + 255 + 255 = 510
    image[0:height//2, 0:width//2] = [0, 0, 255]

    # Top-right quadrant: Pure Green (BGR: 0, 255, 0)
    # Expected divergence: |0-255| + |255-0| + |0-0| = 255 + 255 + 0 = 510
    image[0:height//2, width//2:width] = [0, 255, 0]

    # Bottom-left quadrant: Pure Blue (BGR: 255, 0, 0)
    # Expected divergence: |255-0| + |0-0| + |0-255| = 255 + 0 + 255 = 510
    image[height//2:height, 0:width//2] = [255, 0, 0]

    # Bottom-right quadrant: Pure White (BGR: 255, 255, 255)
    # Expected divergence: |255-255| + |255-255| + |255-255| = 0 + 0 + 0 = 0
    image[height//2:height, width//2:width] = [255, 255, 255]

    # Center circle: Medium Gray (BGR: 128, 128, 128)
    # Expected divergence: |128-128| + |128-128| + |128-128| = 0 + 0 + 0 = 0
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 4
    cv2.circle(image, (center_x, center_y), radius, (128, 128, 128), -1)

    return image

def main():
    print("Starting Chroma Variance project...")

    # Define output file paths
    input_image_path = "input_synthetic_image.png"
    output_divergence_map_path = "output_divergence_map.png"

    # 1. Generate a synthetic input image and save it
    synthetic_image = generate_synthetic_image()
    cv2.imwrite(input_image_path, synthetic_image)
    print(f"Generated and saved synthetic input image: {input_image_path}")

    # 2. Load the static color image
    # cv2.imread loads images in BGR format by default.
    # This step explicitly loads the image from disk, fulfilling the requirement.
    loaded_image = cv2.imread(input_image_path)

    if loaded_image is None:
        print(f"Error: Could not load image from {input_image_path}. Exiting.")
        return

    print(f"Loaded image of shape: {loaded_image.shape}, dtype: {loaded_image.dtype}")

    # 3. Compute the sum of absolute differences between BGR color channels
    # To prevent integer overflow/wrap-around during subtraction, convert channels to int32.
    b_channel = loaded_image[:, :, 0].astype(np.int32)
    g_channel = loaded_image[:, :, 1].astype(np.int32)
    r_channel = loaded_image[:, :, 2].astype(np.int32)

    # Calculate absolute differences for each pair
    diff_bg = np.abs(b_channel - g_channel)
    diff_gr = np.abs(g_channel - r_channel)
    diff_rb = np.abs(r_channel - b_channel)

    # Sum the absolute differences for each pixel to get the raw divergence map
    # The maximum possible value for a pixel is 255*3 = 765, but in practice for
    # 8-bit channels, it's 510 (e.g., (0,0,255) -> |0-0|+|0-255|+|255-0| = 510)
    divergence_map = diff_bg + diff_gr + diff_rb

    print(f"Computed raw divergence map. Min value: {np.min(divergence_map)}, Max value: {np.max(divergence_map)}")

    # 4. Normalize the divergence map to an 8-bit grayscale image (0-255)
    # The output of cv2.normalize is written into the second argument.
    # We create an empty array of the correct shape and type (uint8).
    normalized_divergence_map = np.zeros_like(divergence_map, dtype=np.uint8)
    cv2.normalize(divergence_map, normalized_divergence_map, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    print(f"Normalized divergence map. Min value: {np.min(normalized_divergence_map)}, Max value: {np.max(normalized_divergence_map)}")

    # 5. Save the normalized grayscale divergence map
    cv2.imwrite(output_divergence_map_path, normalized_divergence_map)
    print(f"Saved normalized grayscale color divergence map: {output_divergence_map_path}")

    print("Chroma Variance project finished successfully.")

if __name__ == "__main__":
    main()