
import os

# 저장할 파일 이름
output_filename = "../../라벨링데이터_230515_add/2021_Fashion_val_labels_v230428/Ic_file_names.txt"

# 탐색할 디렉토리 경로
directory_path = "./Ic"

# 디렉토리 경로가 유효한지 확인
if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
    print(f"경로 '{directory_path}'가 존재하지 않거나 디렉토리가 아닙니다.")
else:
    # 디렉토리 안의 모든 파일 이름 가져오기
    file_names = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # 파일 이름에서 확장자를 제거하고 파일 이름만 추가
            file_name_without_extension = os.path.splitext(file)[0]
            file_names.append(file_name_without_extension + ".json")

    # 파일 이름을 텍스트 파일에 저장
    with open(output_filename, "w") as output_file:
        for file_name in file_names:
            output_file.write(file_name + "\n")

    print(f"{len(file_names)} 개의 파일 이름을 '{output_filename}'에 저장했습니다.")
