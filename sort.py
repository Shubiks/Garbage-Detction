import os
import shutil

# Set paths
dataset_dir = r'D:\YoloProject\dataset'  # Root dataset directory
image_dir = os.path.join(dataset_dir, 'images')
label_dir = os.path.join(dataset_dir, 'labels')

# Ensure label directories exist for train, val, and test
def ensure_label_dirs():
    for split in ['train', 'val', 'test']:
        label_split_path = os.path.join(label_dir, split)
        os.makedirs(label_split_path, exist_ok=True)

# Match and copy labels
def match_and_copy_labels():
    for split in ['train', 'val', 'test']:
        image_split_path = os.path.join(image_dir, split)
        label_split_path = os.path.join(label_dir, split)

        if not os.path.exists(image_split_path):
            print(f"Image directory missing: {image_split_path}")
            continue

        for image_name in os.listdir(image_split_path):
            if image_name.endswith('.jpg'):
                label_name = image_name.replace('.jpg', '.txt')
                label_src = os.path.join(label_dir, label_name)  # Assuming all labels are in `labels/`
                label_dest = os.path.join(label_split_path, label_name)

                if os.path.exists(label_src):
                    shutil.copy(label_src, label_dest)
                else:
                    print(f"Missing label for image: {image_name} in {split}")

# Step 1: Ensure label directories exist
ensure_label_dirs()

# Step 2: Match and copy labels
match_and_copy_labels()

print("Labels successfully matched and organized.")
