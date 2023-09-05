import os
import shutil

# 파일명이 나열된 텍스트 파일 경로
input_txt_path = './val_modelfile_json_names.txt'

# 원본 이미지 폴더 경로
input_image_folder = './Model-Pose'

# 새로운 폴더 생성 및 경로 설정
output_folder = './yj_v_org_jg_bf_nm'
os.makedirs(output_folder, exist_ok=True)

# 텍스트 파일에서 파일명 읽어오기
with open(input_txt_path, 'r') as txt_file:
    tops_filenames = txt_file.read().splitlines()

# 원본 이미지 폴더에서 해당 파일을 찾아 새로운 폴더에 복사
for filename in tops_filenames:
    source_path = os.path.join(input_image_folder, filename)
    destination_path = os.path.join(output_folder, filename)

    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f'{filename} 파일을 복사하여 {output_folder}에 저장했습니다.')
    else:
        print(f'{filename} 파일을 {input_image_folder}에서 찾을 수 없습니다.')

print(f'총 {len(tops_filenames)}개의 파일을 {output_folder}에 복사했습니다.')
