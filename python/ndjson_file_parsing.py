import json

# NDJSON 파일을 읽어서 각 라인을 JSON으로 변환
def read_ndjson(file_path):
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    return data

# 데이터 추출 예제
for entry in read_ndjson('C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'):
    print(entry)
