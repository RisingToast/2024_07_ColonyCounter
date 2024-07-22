# data_preprocessing.py

import tensorflow as tf
import numpy as np

def generator_function():
    data = [
        (np.random.rand(100, 100, 3).astype(np.float32), [{'top': 70.0, 'left': 16.0, 'height': 8.0, 'width': 5.0}]),
        (np.random.rand(100, 100, 3).astype(np.float32), [{'top': 30.0, 'left': 33.0, 'height': 28.0, 'width': 20.0}]),
        # Add more data as needed
    ]
    for image, bbox_list in data:
        bbox_array = np.array([list(bbox.values()) for bbox in bbox_list], dtype=np.float32)
        yield image, bbox_array

def preprocess_image(image, bbox):
    image = tf.image.resize(image, [100, 100])
    return image, bbox

def create_datasets(batch_size=32):
    dataset = tf.data.Dataset.from_generator(
        generator_function,
        output_signature=(
            tf.TensorSpec(shape=(100, 100, 3), dtype=tf.float32),
            tf.TensorSpec(shape=(None, 4), dtype=tf.float32)
        )
    )

    dataset = dataset.map(preprocess_image).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    
    # 데이터셋을 훈련과 검증으로 나누기
    dataset_size = sum(1 for _ in dataset)  # 데이터셋의 사이즈 계산
    train_size = int(0.8 * dataset_size)
    validation_size = dataset_size - train_size

    # 훈련 데이터와 검증 데이터로 분리
    train_dataset = dataset.take(train_size)
    validation_dataset = dataset.skip(train_size).take(validation_size)
    
    return train_dataset, validation_dataset

