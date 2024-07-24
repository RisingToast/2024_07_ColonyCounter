import os
import json
import requests
from tqdm import tqdm
import pandas as pd

# ndjson 파일 경로
file_path = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'

# 이미지 저장 디렉토리 경로
image_dir = 'C:/kkt/2024_07_ColonyCounter/down_img'

# 디렉토리가 없으면 생성
os.makedirs(image_dir, exist_ok=True)

# 파일 내용 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    data = [json.loads(line) for line in file]

# 데이터 프레임으로 변환
df = pd.json_normalize(data)

# 이미지 다운로드 함수
def download_images(df, image_dir):
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        image_url = row['data_row.row_data']
        image_id = row['data_row.external_id']
        base_name, ext = os.path.splitext(image_id)
        image_path = os.path.join(image_dir, image_id)
        
        # 이름이 같은 경우 이름에 인덱스를 추가하여 고유한 이름을 생성
        counter = 1
        while os.path.exists(image_path):
            new_name = f"{base_name}_{counter}{ext}"
            image_path = os.path.join(image_dir, new_name)
            counter += 1
        
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Failed to download image: {image_url}, Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image {image_url}: {e}")

# 이미지 다운로드
download_images(df, image_dir)