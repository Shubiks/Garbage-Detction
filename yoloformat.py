import os
from PIL import Image

# Paths to the images and labels directories
images_dir = r'D:\YoloProject\dataset\images'  # Directory containing images (train/val/test)
labels_dir = r'D:\YoloProject\dataset\labels'  # Directory containing corresponding .txt files

# Function to normalize the annotations
def normalize_labels(image_path, label_path):
    # Open the image to get dimensions
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Read and normalize the label file
    with open(label_path, 'r') as file:
        lines = file.readlines()

    normalized_lines = []
    for line in lines:
        data = line.strip().split()
        if len(data) == 5:  # Check if the line has the correct format
            cls_id, x_center, y_center, width, height = map(float, data)
            
            # Normalize values
            x_center /= img_width
            y_center /= img_height
            width /= img_width
            height /= img_height

            # Save normalized annotation
            normalized_lines.append(f"{int(cls_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        else:
            print(f"Skipping invalid line in {label_path}: {line.strip()}")

    # Overwrite the file with normalized data
    with open(label_path, 'w') as file:
        file.write('\n'.join(normalized_lines))

    print(f"Normalization completed for {label_path}")

# Iterate through all subdirectories (train/val/test)
for split in ['train', 'val', 'test']:
    split_image_dir = os.path.join(images_dir, split)
    split_label_dir = os.path.join(labels_dir, split)

    for category in os.listdir(split_image_dir):
        image_category_path = os.path.join(split_image_dir, category)
        label_category_path = os.path.join(split_label_dir, category)

        # Ensure the current category is a directory
        if not os.path.isdir(image_category_path):
            continue

        # Process each image and its corresponding label file
        for image_name in os.listdir(image_category_path):
            if image_name.endswith('.jpg'):
                image_path = os.path.join(image_category_path, image_name)
                label_path = os.path.join(label_category_path, image_name.replace('.jpg', '.txt'))

                if os.path.exists(label_path):
                    print(f"Normalizing {label_path} based on {image_path}")
                    normalize_labels(image_path, label_path)
                else:
                    print(f"Label file for {image_name} not found. Skipping.")

print("Normalization complete!")
