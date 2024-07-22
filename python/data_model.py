import json
import tensorflow as tf
import json
import numpy as np


def read_ndjson_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

# Usage example
file_path = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'
for entry in read_ndjson_file(file_path):
    print(entry)

def parse_annotation_data(data):
    for entry in data:
        try:
            # Extract the relevant fields
            image_url = entry.get("data_row", {}).get("row_data", "")
            annotations = entry.get("projects", {}).get("clynqj52408k707zxhge54g8q", {}).get("labels", [])[0].get("annotations", {}).get("objects", [])
            
            # Process each annotation
            for annotation in annotations:
                bbox = annotation.get("bounding_box", {})
                print(f"Image URL: {image_url}")
                print(f"Bounding Box: {bbox}")
        
        except KeyError as e:
            print(f"Missing key: {e}")

# Usage example
file_path = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'
data = read_ndjson_file(file_path)
parse_annotation_data(data)

def parse_annotation(annotation):
    image_url = annotation.get("data_row", {}).get("row_data", "")
    objects = annotation.get("projects", {}).get("clynqj52408k707zxhge54g8q", {}).get("labels", [])[0].get("annotations", {}).get("objects", [])
    bounding_boxes = [
        obj.get("bounding_box", {}) for obj in objects
    ]
    return image_url, bounding_boxes

# Example generator function
def generator_function():
    # Example data: List of tuples (image, bounding boxes)
    data = [
        (np.random.rand(100, 100, 3).astype(np.float32), [{'top': 70.0, 'left': 16.0, 'height': 8.0, 'width': 5.0}]),
        # Add more data as needed
    ]
    for image, bbox_list in data:
        # Convert bounding boxes to numpy array
        bbox_array = np.array([list(bbox.values()) for bbox in bbox_list], dtype=np.float32)
        yield image, bbox_array

# Create dataset
dataset = tf.data.Dataset.from_generator(
    generator_function,
    output_signature=(
        tf.TensorSpec(shape=(100, 100, 3), dtype=tf.float32),  # Adjust shape and dtype as needed
        tf.TensorSpec(shape=(None, 4), dtype=tf.float32)         # Adjust shape and dtype as needed
    )
)

# Example usage
for image, bbox in dataset.take(1):
    print(image.shape, bbox.shape)

for image, bbox in train_dataset.take(1):
    print(f"Image shape: {image.shape}")
    print(f"Bounding boxes shape: {bbox.shape}")