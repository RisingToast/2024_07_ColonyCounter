import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import tensorflow as tf

# 모델 로드
model_path = 'C:/kkt/2024_07_ColonyCounter/min_model/min_colony.keras'
model = tf.keras.models.load_model(model_path)

# 콜로니 검출 및 시각화 함수
def detect_and_visualize(image_path, model):
    original_image = Image.open(image_path).convert("RGB")  # RGBA를 RGB로 변환
    image = original_image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    bbox = predictions[0]
    
    # bounding box 좌표를 원래 이미지 크기에 맞게 변환
    img_width, img_height = original_image.size
    bbox = [
        bbox[0] * img_width,
        bbox[1] * img_height,
        bbox[2] * img_width,
        bbox[3] * img_height
    ]

    # 원래 이미지에 bounding box 시각화
    draw = ImageDraw.Draw(original_image)
    draw.rectangle(
        [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]],
        outline="red",
        width=3
    )

    plt.imshow(original_image)
    plt.axis('off')  # 축 숨기기
    plt.show()

# 예시 이미지 경로
example_image_path = 'C:/kkt/2024_07_ColonyCounter/Colony_Image/05.E.coli.jpg'
detect_and_visualize(example_image_path, model)