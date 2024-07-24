import tensorflow as tf

# 모델의 입력과 출력에 필요한 값들을 정의합니다.
IMAGE_HEIGHT = 128  # 예시: 이미지 높이
IMAGE_WIDTH = 128   # 예시: 이미지 너비
CHANNELS = 3        # RGB 이미지의 경우 3
NUM_CLASSES = 10    # 예시: 10개의 클래스

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model
