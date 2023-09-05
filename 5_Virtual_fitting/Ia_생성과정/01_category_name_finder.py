import os
import json

# JSON 파일들이 있는 폴더 경로
folder_path = './Item-Parse/'

# 폴더 내의 모든 JSON 파일 찾기
json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# 모든 JSON 파일 내의 category_name과 category_id 추출
category_info = {}  # 카테고리 정보를 저장할 딕셔너리

for json_file in json_files:
    json_path = os.path.join(folder_path, json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)
        for region_key, region_data in data.items():
            if region_key != 'file_name' and isinstance(region_data, dict):
                category_name = region_data.get('category_name')
                category_id = region_data.get('category_id')
                if category_name and category_id is not None:
                    category_info[category_name] = category_id

# 카테고리 이름과 ID 출력
print("Category information:")
for name, id in category_info.items():
    print(f"Name: {name}, ID: {id}")
