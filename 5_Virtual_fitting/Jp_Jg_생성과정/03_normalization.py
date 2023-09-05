import os
import json

def normalize_keypoints(keypoints, image_width, image_height):
    normalized_keypoints = []

    for i in range(0, len(keypoints), 3):
        x = keypoints[i]
        y = keypoints[i + 1]
        v = keypoints[i + 2]

        normalized_x = x / image_width
        normalized_y = y / image_height

        normalized_keypoints.extend([normalized_x, normalized_y, v])

    return normalized_keypoints

input_folder = './yj_v_org_jg_bf_nm'
output_folder = './Jp'  # 변경 가능한 출력 폴더 경로

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 폴더 내의 모든 JSON 파일 찾기
json_files = [file for file in os.listdir(input_folder) if file.endswith('.json')]

for json_file in json_files:
    json_path = os.path.join(input_folder, json_file)
    output_path = os.path.join(output_folder, json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)

        image_width = data['image_size']['width']
        image_height = data['image_size']['height']

        normalized_keypoints = normalize_keypoints(data['landmarks'], image_width, image_height)
        data['landmarks'] = normalized_keypoints

    with open(output_path, 'w') as file:
        json.dump(data, file)

    print(f'Normalized keypoints saved to {output_path}')
