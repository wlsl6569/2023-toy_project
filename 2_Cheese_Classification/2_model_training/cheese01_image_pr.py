import os
import shutil
import glob
from sklearn.model_selection import train_test_split
'''
파일 구조 아래와 같이 만든다
cheese_dataset 
 ㄴdata
   ㄴblue/camembert/cheddar/emmental
'''
class ImageMove :
    def __init__(self, org_folder):
        self.org_folder = org_folder
    def move_images(self):
        file_path_list = glob.glob(os.path.join(self.org_folder, "*" , "*.png"))
        for file_path in file_path_list :
            folder_name = file_path.split("\\")[1]
            if folder_name == "blue" :
                shutil.move(file_path, "./cheese_dataset/data/blue")
            elif folder_name == "camembert" :
                shutil.move(file_path, "./cheese_dataset/data/camembert")
            elif folder_name == "cheddar" :
                shutil.move(file_path, "./cheese_dataset/data/cheddar")
            elif folder_name == "emmental" :
                shutil.move(file_path, "./cheese_dataset/data/emmental")

'''
함수 실행 
'''
#test = ImageMove("./final_cheese_data/")
#test.move_images()


'''
이제 파일 구조 만들 일 없이 그냥 돌리면 된다.
'''

class ImageDataMove:
    def __init__(self, org_dir, train_dir, val_dir):
        self.org_dir = org_dir
        self.train_dir = train_dir
        self.val_dir = val_dir

    def move_images(self):
        # 파일 경로 리스트 가져오기
        file_path_list01 = glob.glob(os.path.join(self.org_dir, "*", "blue", "*.png"))
        file_path_list02 = glob.glob(os.path.join(self.org_dir, "*", "camembert", "*.png"))
        file_path_list03 = glob.glob(os.path.join(self.org_dir, "*", "cheddar", "*.png"))
        file_path_list04 = glob.glob(os.path.join(self.org_dir, "*", "emmental", "*.png"))

        # 데이터 분할
        bl_train_data_list, bl_val_data_list = train_test_split(file_path_list01, test_size=0.2)
        cm_train_data_list, cm_val_data_list = train_test_split(file_path_list02, test_size=0.2)
        ch_train_data_list, ch_val_data_list = train_test_split(file_path_list03, test_size=0.2)
        em_train_data_list, em_val_data_list = train_test_split(file_path_list03, test_size=0.2)

        # 파일 이동
        self.copy_files(bl_train_data_list, os.path.join(self.train_dir, "blue"))
        self.copy_files(bl_val_data_list, os.path.join(self.val_dir, "blue"))
        self.copy_files(cm_train_data_list, os.path.join(self.train_dir, "camembert"))
        self.copy_files(cm_val_data_list, os.path.join(self.val_dir, "camembert"))
        self.copy_files(ch_train_data_list, os.path.join(self.train_dir, "cheddar"))
        self.copy_files(ch_val_data_list, os.path.join(self.val_dir, "cheddar"))
        self.copy_files(em_train_data_list, os.path.join(self.train_dir, "emmental"))
        self.copy_files(em_val_data_list, os.path.join(self.val_dir, "emmental"))

    def copy_files(self, file_list, mov_dir):
        os.makedirs(mov_dir, exist_ok=True)
        for file_path in file_list:
            shutil.copy2(file_path, mov_dir)

org_dir = "cheese_dataset"
train_dir = "./cheese_data/train"
val_dir = "./cheese_data/val"

'''
move_temp = ImageDataMove(org_dir, train_dir, val_dir)
move_temp.move_images()
'''