01_extract_ic_or_ia_info_to_list.py : 뽑아둔 Ic(또는 Ia)의 파일 리스트 txt파일로 뽑기(이때 jpg 확장자를 json으로 변경하여 저장시킴)
02_save_from_list.py : 만든 리스트를 통해서 원본 pose/item 데이터 중 사용되는 JSON 파일만 따로 뽑아 저장시키기
(= Ic에 사용되는 상의 이미지 관련된 json이나 Ia에 사용되는 정면 이미지 관련 json만 사용한다는 뜻)
03_normalization.py : 0~1사이로 키포인트 값 정규화 (Jp, Jg)