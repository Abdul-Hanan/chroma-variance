# Chroma Variance

Generates a grayscale map showing the per-pixel variance between BGR color channels.

## What it Does

This project takes a color image, computes a "color divergence" value for each pixel, and saves this as a normalized grayscale image. The divergence for a pixel `(B, G, R)` is calculated as `|B-G| + |G-R| + |R-B|`. Pixels with highly differing channel values (e.g., pure red, green, or blue) will show high divergence (brighter in the output map), while pixels with similar channel values (e.g., grayscale, white, or black) will show low divergence (darker).

The script includes a small synthetic image generator to ensure it runs standalone without requiring any external files.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute the script:**
    ```bash
    python main.py
    ```

## Output

Upon successful execution, the script will generate two image files in the same directory:
-   `input_synthetic_image.png`: The color image generated internally, used as input.
-   `output_divergence_map.png`: The resulting grayscale image showing the color divergence.