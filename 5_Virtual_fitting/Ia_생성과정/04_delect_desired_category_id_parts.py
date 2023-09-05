import os
import json
from PIL import Image, ImageDraw
from carvekit.api.high import HiInterface

# JSON 파일들이 있는 폴더 경로
json_folder_path = '../../라벨링데이터_230515_add/2021_Fashion_train_labels_v230428/Model-Parse'
input_folder = './combined_Model-Image/'
output_folder = './delected_Model-Image02'  # 변경 가능한 출력 폴더 경로

# 출력 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 폴더 내의 모든 JSON 파일 찾기
json_files = [file for file in os.listdir(json_folder_path) if file.endswith('.json')]

# 원하는 category_id들
desired_category_ids = [9, 7, 8]

# JSON 파일을 이용하여 이미지 처리 및 저장
for json_file in json_files:
    json_path = os.path.join(json_folder_path, json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)
        jpg_filename = json_file[:-5] + '.jpg'  # JSON 파일 이름으로부터 JPG 파일 이름 생성
        image_filename = os.path.join(input_folder, jpg_filename)  # JPG 파일 경로 구성

        if os.path.exists(image_filename):
            img = Image.open(image_filename)
            img = img.convert("RGBA")

            # 이미지에 해당하는 카테고리 영역을 desired_category_ids의 색상으로 채우기
            draw = ImageDraw.Draw(img)

            for region_key, region_data in data.items():
                if region_key == 'file_name':
                    continue
                category_id = region_data.get('category_id')

                if category_id in desired_category_ids:
                    segmentation = region_data.get('segmentation', [])

                    for segment in segmentation:
                        points = [(x, y) for x, y in segment]

                        # 세그먼트 색칠하기
                        draw.polygon(points, outline=None, fill=(130, 130, 130, 130))  # 회색(반투명)으로 설정

                        # 세그먼트 테두리 그리기
                        draw.line(points + [points[0]], fill=(130, 130, 130, 130), width=5)  # 회색(반투명) 테두리, 너비 5px

            # 이미지 저장
            output_path = os.path.join(output_folder, jpg_filename)
            img.save(output_path, format='PNG')  # PNG 포맷으로 저장
            print('Processed image saved as', output_path)
        else:
            print(f'Image not found: {image_filename}')
