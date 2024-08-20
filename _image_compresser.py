import os
from PIL import Image

# Define the input and output directories
input_dir = 'assets_original_images'
output_dir = 'assets'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each image in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):  # Adjust extensions as needed
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Skip processing if the file already exists in the output directory
        if os.path.exists(output_path):
            print(f"Skipping {filename}, already exists in the output directory.")
            continue

        # Open the image, resize it, and save it to the output directory
        with Image.open(input_path) as img:
            resized_img = img.resize((64, 48))
            resized_img.save(output_path)
            print(f"Processed and saved {filename} to {output_dir}.")

print("Processing completed.")
