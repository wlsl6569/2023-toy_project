import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models import vgg11, VGG11_Weights
from torch.optim import AdamW
from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torch.nn as nn
from cheese02_customdataset import CustomDataset
from tqdm import tqdm

def train(model, train_loader, val_loader, epochs, DEVICE, optimizer, criterion) :
    best_val_acc = 0.0
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []
    print("Train...")
    for epoch in range(epochs) :
        train_loss = 0.0
        val_loss = 0.0
        val_acc = 0.0
        train_acc = 0.0

        model.train()

        # tqdm
        train_loader_iter = tqdm(train_loader,
                                 desc=f"Epoch {epoch +1}/{epochs}", leave=False)

        for i, (data, target) in enumerate(train_loader_iter) :
            data = data.to(DEVICE)
            target = target.to(DEVICE)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

            # acc
            _, pred = torch.max(output, 1)
            train_acc += (pred == target).sum().item()

            # print the loss
            if i % 10 == 9 :
               train_loader_iter.set_postfix({"Loss" : loss.item()})

        train_loss /= len(train_loader)
        train_acc = train_acc / len(train_loader.dataset)

        # eval
        model.eval()
        with torch.no_grad() :
            for data, target in val_loader :
                data = data.to(DEVICE)
                target = target.to(DEVICE)

                outputs = model(data)
                pred = outputs.argmax(dim=1, keepdim=True)
                val_acc += pred.eq(target.view_as(pred)).sum().item()
                val_loss += criterion(outputs, target).item()

        val_loss /= len(val_loader)
        val_acc = val_acc / len(val_loader.dataset)

        train_losses.append(train_loss)
        train_accs.append(train_acc)
        val_losses.append(val_loss)
        val_accs.append(val_acc)

        # save the model with the best val acc
        if val_acc > best_val_acc :
            torch.save(model.state_dict(), 'best_cheese_model.pt')
            best_val_acc = val_acc

        print(f"Epoch [{epoch + 1}/{epochs}], "
              f"Train Loss : {train_loss :.4f}, "
              f"Train Acc : {train_acc:.4f}, "
              f"Val Loss : {val_loss :.4f},"
              f" Val Acc : {val_acc :.4f}  ")

    return model, train_losses, val_losses, train_accs, val_accs

def main() :
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # DEVICE_MPS = torch.device("mps") # mac m1 or m2

    model = vgg11(weights=VGG11_Weights.DEFAULT)
    num_feature = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(num_feature, 4)
    model.to(DEVICE)

    """
    # transforms
    1. aug 
    2. ToTensor 
    3. Normalize
    """
    train_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor()
    ])

    # dataset
    train_dataset = CustomDataset("./cheese_data/train/", transform=train_transform)
    val_dataset = CustomDataset("./cheese_data/val/", transform=val_transform)

    # dataloader
    train_loader = DataLoader(train_dataset, batch_size=100, num_workers=4,
                              pin_memory=True, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=100, num_workers=4,
                            pin_memory=True, shuffle=False)
    # import time
    # import math
    # test = time.time()
    # math.factorial(100000)
    # test01 = time.time()
    # print(f"{test01 - test :.5f} sec")

    epochs = 100
    criterion = CrossEntropyLoss().to(DEVICE)
    optimizer = AdamW(model.parameters(), lr=0.001, weight_decay=1e-2)

    train(model, train_loader, val_loader, epochs, DEVICE, optimizer, criterion)

if __name__ == "__main__" :
    main()