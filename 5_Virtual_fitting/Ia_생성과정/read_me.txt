01_category_name_finder.py : Model-Parse에서 쓰인 category_id 정보 추출
02_mask_maker : model.py :  이미지에서 배경 부분 흑백마스크 생성
03_bg_delect_using_mask.py  : 배경 흑백 마스크로 model 이미지에서 배경제거
04_delect_desired_category_id_parts.py : 배경 제거된 이미지에서 원하는 영역 정보 제거 (Ia 생성완료)
05_frontimage_classify.py : 파일 이름이'000'로 끝나는 이미지만 골라내서 따로 저장(000은 정면 이미지), 이름이 000이 아닌 정면이미지는 수작업으로 골라냄


