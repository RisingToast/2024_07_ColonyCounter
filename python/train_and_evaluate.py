import tensorflow as tf
import numpy as np
from model_definition import create_model
from data_preprocessing import create_datasets  # 데이터셋 생성 함수 가져오기

def get_dataset():
    def generator_function():
        data = [
            (np.random.rand(100, 100, 3).astype(np.float32), [{'top': 70.0, 'left': 16.0, 'height': 8.0, 'width': 5.0}]),
            # 추가 데이터가 필요한 경우 여기에 추가
        ]
        for image, bbox_list in data:
            bbox_array = np.array([list(bbox.values()) for bbox in bbox_list], dtype=np.float32)
            yield image, bbox_array

    dataset = tf.data.Dataset.from_generator(
        generator_function,
        output_signature=(
            tf.TensorSpec(shape=(100, 100, 3), dtype=tf.float32),
            tf.TensorSpec(shape=(None, 4), dtype=tf.float32)
        )
    )

    dataset = dataset.batch(32)

    # 데이터셋의 총 샘플 수를 계산하는 방법
    dataset_size = sum(1 for _ in dataset)
    train_size = int(0.8 * dataset_size)
    validation_size = dataset_size - train_size

    train_dataset = dataset.take(train_size)
    validation_dataset = dataset.skip(train_size).take(validation_size)

    return train_dataset, validation_dataset

# 데이터셋 불러오기
train_dataset, validation_dataset = get_dataset()

# 모델 정의
input_shape = (100, 100, 3)
model = create_model(input_shape)

# 모델 훈련
model.fit(train_dataset, epochs=10, validation_data=validation_dataset)

# 모델 평가
evaluation = model.evaluate(validation_dataset)
print('Evaluation results:', evaluation)
