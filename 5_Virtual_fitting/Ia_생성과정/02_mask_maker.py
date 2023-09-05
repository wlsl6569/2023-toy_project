import os
import json
from PIL import Image, ImageDraw

# JSON 파일들이 있는 폴더 경로
json_folder_path = '../../라벨링데이터_230515_add/2021_Fashion_train_labels_v230428/Model-Parse'
input_folder = '../2021_Fashion_train_model02/Model-Image/'
output_folder = './Model-msk'  # 변경 가능한 출력 폴더 경로

# 출력 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 폴더 내의 모든 JSON 파일 찾기
json_files = [file for file in os.listdir(json_folder_path) if file.endswith('.json')]

# ... (이전 코드 부분은 삭제)

# JSON 파일을 이용하여 이미지 처리 및 저장
for json_file in json_files:
    json_path = os.path.join(json_folder_path, json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)
        jpg_filename = json_file[:-5] + '.jpg'  # JSON 파일 이름으로부터 JPG 파일 이름 생성
        image_filename = os.path.join(input_folder, jpg_filename)  # JPG 파일 경로 구성

        if os.path.exists(image_filename):
            img = Image.open(image_filename)
            img_width, img_height = img.size

            # 이미지 크기로 새 이미지 생성하고 투명하게 설정
            mask = Image.new('L', (img_width, img_height), 0)
            draw = ImageDraw.Draw(mask)

            for region_key, region_data in data.items():
                if region_key == 'file_name':
                    continue

                segmentation = region_data.get('segmentation', [])

                for segment in segmentation:
                    points = [(x, y) for x, y in segment]

                    # desired_category_ids에 해당하지 않는 부분을 흰색으로 채우기
                    draw.polygon(points, outline=None, fill=255)

            # 마스크 이미지 저장
            mask_path = os.path.join(output_folder, json_file[:-5] + '_mask.png')
            mask.save(mask_path, format='PNG')  # PNG 포맷으로 저장
            print('처리된 마스크 이미지 저장됨:', mask_path)
        else:
            print(f'이미지를 찾을 수 없음: {image_filename}')
