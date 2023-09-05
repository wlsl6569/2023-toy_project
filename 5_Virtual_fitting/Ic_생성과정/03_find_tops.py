
mport os
import json

# 경로 설정
json_folder_path = '../../라벨링데이터_230515_add/2021_Fashion_train_labels_v230428/Item-Parse'

# "tops"인 파일명을 저장할 리스트 초기화
tops_filenames = []

# 폴더 내의 모든 JSON 파일 찾기
json_files = [file for file in os.listdir(json_folder_path) if file.endswith('.json')]

# JSON 파일을 읽어서 "category_name"이 "tops"인 경우 파일명 저장
for json_file in json_files:
    json_path = os.path.join(json_folder_path, json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)
        category_name = data.get('category_name', '')

        if category_name == "tops":
            tops_filenames.append(json_file)

# 파일명을 확장자를 jpg로 변경하여 텍스트 파일에 저장
output_txt_path = 'tops_filenames.txt'

with open(output_txt_path, 'w') as output_file:
    for filename in tops_filenames:
        jpg_filename = filename[:-5] + '.jpg'  # JSON 파일 이름으로부터 JPG 파일 확장자 생성
        output_file.write(jpg_filename + '\n')

print(f'{len(tops_filenames)}개의 "tops" 카테고리 파일명이 {output_txt_path}에 저장되었습니다.')
