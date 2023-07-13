import os

from torch.utils.data import Dataset
from PIL import Image
import glob

class CustomDataset(Dataset) :
    def __init__(self, data_dir, transform=None):
        # data_dir = ./data/train/
        self.data_dir = glob.glob(os.path.join(data_dir, "*", "*.png"))
        self.transform = transform
        self.label_dict = {"blue" : 0 , "camembert" : 1, "cheddar" : 2, "emmental" : 3}

    def __getitem__(self, item):
        image_path = self.data_dir[item]
        #image_path >>> ./data/train\waveshow\rock.00006_augmented_noise.png
        image = Image.open(image_path)
        image = image.convert("RGB")
        label_name = image_path.split("\\")[1]
        label = self.label_dict[label_name]

        if self.transform is not None :
            image = self.transform(image)

        return image ,label

    def __len__(self):
        return len(self.data_dir)
