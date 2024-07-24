import tensorflow as tf
from pycocotools.coco import COCO
import numpy as np
import cv2
import os

def load_coco_data(coco_json_file, image_dir):
    # COCO JSON 파일을 로드
    coco = COCO(coco_json_file)
    img_ids = coco.getImgIds()

    def load_image(image_id):
        img_info = coco.loadImgs(image_id)[0]
        img_path = os.path.join(image_dir, img_info['file_name'])
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at path: {img_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # TensorFlow는 RGB 이미지를 사용
        img = tf.image.resize(img, [100, 100])     # 원하는 사이즈로 조정
        img = img / 255.0                          # 정규화
        return img

    def load_label(image_id):
        ann_ids = coco.getAnnIds(imgIds=image_id)
        anns = coco.loadAnns(ann_ids)
        bboxes = []
        for ann in anns:
            bbox = ann['bbox']  # [x, y, width, height]
            bbox.append(ann['category_id'])  # 클래스 레이블 추가
            bboxes.append(bbox)
        return np.array(bboxes, dtype=np.float32)

    def py_load_data(image_id):
        # Convert image_id to string if it's not already
        image_id_str = image_id.numpy().decode('utf-8') if isinstance(image_id.numpy(), bytes) else str(image_id.numpy())
        image = load_image(image_id_str)
        labels = load_label(image_id_str)
        return image, labels

    # TensorFlow 데이터셋 생성
    dataset = tf.data.Dataset.from_tensor_slices(img_ids)
    dataset = dataset.map(lambda img_id: tf.py_function(func=py_load_data, inp=[img_id], Tout=[tf.float32, tf.float32]))

    return dataset

# 예시 사용법
coco_json_file = 'C:/kkt/2024_07_ColonyCounter/JSON_File/output_file.json'
image_dir = 'C:/kkt/2024_07_ColonyCounter/Images/'  # 실제 이미지가 저장된 경로
dataset = load_coco_data(coco_json_file, image_dir)

# 데이터셋을 배치 및 기타 전처리
dataset = dataset.batch(32).prefetch(tf.data.AUTOTUNE)



