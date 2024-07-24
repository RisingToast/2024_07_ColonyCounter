import tensorflow as tf
import json
from pycocotools.coco import COCO
import os

def load_image(image_id, coco):
    print(f"Loading image with ID: {image_id} (type: {type(image_id)})")
    try:
        # Check if image_id exists in coco dataset
        if image_id not in coco.imgs:
            raise KeyError(f"Image ID {image_id} not found in dataset.")
        
        # Load image info
        img_info = coco.loadImgs(image_id)[0]
    except KeyError as e:
        print(f"KeyError: {e}. This image ID might not be in the COCO dataset.")
        return None

    img_path = img_info['file_name']
    
    # Construct image path
    img_path = os.path.join('C:/kkt/2024_07_ColonyCounter/Images/', img_path)  # Adjust path to your images
    if not os.path.isfile(img_path):
        raise ValueError(f"Image file not found: {img_path}")

    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH))
    img = tf.keras.preprocessing.image.img_to_array(img)
    return img

def create_dataset():
    coco = COCO('C:/kkt/2024_07_ColonyCounter/JSON_File/output_file.json')  # Adjust path to your annotations file
    
    def generator():
        image_ids = coco.getImgIds()
        for image_id in image_ids:
            img = load_image(image_id, coco)
            if img is not None:
                yield img, 0  # Replace with actual label or annotation
    
    dataset = tf.data.Dataset.from_generator(generator, output_signature=(
        tf.TensorSpec(shape=(IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS), dtype=tf.float32),
        tf.TensorSpec(shape=(), dtype=tf.int32)
    ))
    
    return dataset
