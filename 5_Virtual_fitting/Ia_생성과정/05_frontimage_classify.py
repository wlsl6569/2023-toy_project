import os
import shutil

# 원본 이미지 디렉토리 경로
source_directory = './delected_Model-Image02'

# 결과 이미지를 저장할 디렉토리 경로
output_directory = './Ia'  # 변경 가능한 출력 폴더 경로

# 출력 폴더 생성
os.makedirs(output_directory, exist_ok=True)

# 원본 이미지 디렉토리에서 이미지 파일 목록 가져오기
image_files = [file for file in os.listdir(source_directory) if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

# 두 번째 언더바 뒤에 숫자가 "000"인 이미지 파일을 찾아서 복사
for image_file in image_files:
    parts = image_file.split('_')

    if len(parts) >= 3 and parts[-1].split('.')[0] == '000':
        source_path = os.path.join(source_directory, image_file)
        output_path = os.path.join(output_directory, image_file)

        # 이미지 파일을 복사
        shutil.copy(source_path, output_path)
        print(f'이미지 복사됨: {output_path}')