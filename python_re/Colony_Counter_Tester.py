import os
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# ndjson 파일 경로
file_path = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'

# 이미지 저장 디렉토리 경로
image_dir = 'C:/kkt/2024_07_ColonyCounter/down_img'

# 파일 내용 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

# 데이터 프레임으로 변환
df = pd.json_normalize(data)

# 이미지와 라벨 데이터를 로드하는 함수
def load_data(df, image_dir):
    images = []
    labels = []
    for index, row in df.iterrows():
        image_id = row['data_row.external_id']
        base_name, ext = os.path.splitext(image_id)
        image_path = os.path.join(image_dir, image_id)
        
        # 이름이 같은 경우의 처리된 파일명 확인
        counter = 1
        while not os.path.exists(image_path) and counter < 100:
            new_name = f"{base_name}_{counter}{ext}"
            image_path = os.path.join(image_dir, new_name)
            counter += 1
        
        if not os.path.exists(image_path):
            print(f"Image not found: {image_path}")
            continue
        
        try:
            image = Image.open(image_path).resize((224, 224))
            image_array = np.array(image) / 255.0
            images.append(image_array)

            labels_list = row.get('projects.clynqj52408k707zxhge54g8q.labels', [])
            if labels_list:
                annotations = labels_list[0].get('annotations', {})
                objects = annotations.get('objects', [])
                for colony in objects:
                    bounding_box = colony.get('bounding_box', {})
                    top = bounding_box.get('top', 0)
                    left = bounding_box.get('left', 0)
                    height = bounding_box.get('height', 0)
                    width = bounding_box.get('width', 0)

                    # bounding box 좌표를 이미지 크기에 맞게 조정
                    bbox = [
                        left / 100,
                        top / 100,
                        width / 100,
                        height / 100
                    ]
                    labels.append(bbox)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
    
    return np.array(images), np.array(labels)

# 데이터 로드
train_images, train_labels = load_data(df, image_dir)

# 총 이미지 수 출력
print(f"Total number of images: {len(train_images)}")

if len(train_images) == 0:
    print("No images loaded. Please check the data loading process.")
else:
    # 딥러닝 모델 생성
    def create_model():
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(4, activation='sigmoid')  # bounding box output: [x, y, width, height]
        ])
        
        model.compile(optimizer=Adam(), loss='mean_squared_error')
        return model

    model = create_model()
    model.summary()

    # 모델 학습
    if len(train_labels) > 0:
        model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_split=0.2)
        # 모델 저장
        model_save_path = 'C:/kkt/2024_07_ColonyCounter/model/min_colony.keras'
        tf.keras.models.save_model(model, model_save_path)
        print(f"Model saved successfully to {model_save_path}.")
    else:
        print("No labels loaded. Please check the data loading process.")