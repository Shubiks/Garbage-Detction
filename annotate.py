import os
import torch
from PIL import Image

dataset_dir = r'D:\YoloProject\dataset\images'  # Path to your image directory
output_dir = r'D:\YoloProject\dataset\labels'  # Path to save label files

# Load pre-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use small YOLOv5 model (yolov5s)

# Function to save YOLO annotations in .txt format
def save_yolo_labels(pred, img_name, output_dir):
    # Create a .txt file for every image
    label_file = os.path.join(output_dir, img_name.replace('.jpg', '.txt'))

    if pred is not None and len(pred) > 0:
        with open(label_file, 'w') as f:
            # Loop through all detections in the prediction
            for det in pred:
                # Extract coordinates and class ID
                x_center, y_center, width, height, conf, cls_id = det
                cls_id = int(cls_id.item())  # Class ID as integer

                # Normalize by image width and height
                label = f"{cls_id} {x_center.item()} {y_center.item()} {width.item()} {height.item()}"
                f.write(label + '\n')
    else:
        # No detections: Return False to indicate no objects found
        return False

    # If detections exist, return True
    return True

# Loop through all categories and process images
for category in os.listdir(dataset_dir):
    category_path = os.path.join(dataset_dir, category)
    
    for image_name in os.listdir(category_path):
        if image_name.endswith('.jpg'):
            print(f"Processing image: {image_name}")

            # Load image
            img_path = os.path.join(category_path, image_name)
            img = Image.open(img_path)
            
            # Run inference using YOLOv5
            results = model(img)
            results.print()  # Print results to see predictions

            # Extract predictions (convert predictions to a list of detections)
            pred = results.xywh[0]  # Get predictions as (x_center, y_center, width, height, conf, cls_id)

            # Save YOLO format annotations or remove image if no objects detected
            annotations_created = save_yolo_labels(pred, image_name, output_dir)

            # If no annotations were created, delete the image
            if not annotations_created:
                print(f"No objects detected in {image_name}. Removing image.")
                os.remove(img_path)

print("Annotation generation complete!")
