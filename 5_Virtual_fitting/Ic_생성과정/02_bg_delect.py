from PIL import Image, ImageDraw, ImageChops
import os
import json

# 원본 이미지 폴더 경로
input_folder = './Item-top-Image/'

# 마스크 폴더 경로
mask_folder = './Item-msk/'

# 결과 이미지 저장 폴더 경로
output_folder = './Ic'  # 변경 가능한 출력 폴더 경로

# 출력 폴더 생성
os.makedirs(output_folder, exist_ok=True)



# 원본 이미지 파일 리스트 가져오기
image_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

# 이미지와 마스크를 합치고 검은 부분을 (130, 130, 130, 130) 컬러로 만들어 저장
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    mask_file = image_file[:-4] + '_mask.jpg'  # 예: image.jpg -> image_mask.png
    mask_path = os.path.join(mask_folder, mask_file)

    if os.path.exists(mask_path):
        img = Image.open(image_path).convert("RGBA")
        mask = Image.open(mask_path).convert("L")

        # 합쳐진 이미지 생성
        combined_img = ImageChops.composite(img, Image.new("RGBA", img.size, (130, 130, 130, 130)), mask)


        # 라인 사이즈 변경
        draw = ImageDraw.Draw(combined_img)
        line_width = 6
        draw.rectangle(
            [(line_width, line_width), (combined_img.width - line_width, combined_img.height - line_width)],
            outline=(130, 130, 130, 130),
            width=line_width
        )

        # 합쳐진 이미지 저장
        combined_path = os.path.join(output_folder, image_file[:-4] + '.jpg')
        combined_img.save(combined_path, format='PNG')  # PNG 포맷으로 저장
        print('마스크를 사용하여 합쳐진 이미지 저장됨:', combined_path)
    else:
        print(f'마스크 이미지를 찾을 수 없음: {mask_path}')
