import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms
from torch.autograd import Variable
import torch.optim as optim

from models import *
from utils.utils import *
from utils.datasets import *
from utils.parse_config import *

import argparse

if __name__ == "__main__":
    torch.cuda.empty_cache()

    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100, help="number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="size of each image batch")
    parser.add_argument("--model_def", type=str, default="trainer/config/yolov3-custom.cfg", help="path to model definition file")
    parser.add_argument("--data_config", type=str, default="trainer/config/custom.data", help="path to data config file")
    opt = parser.parse_args()
    pretrained_weights = None

    img_size = 416
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Get data configuration
    data_config = parse_data_config(opt.data_config)
    train_path = data_config["train"]
    valid_path = data_config["valid"]
    class_names = load_classes(data_config["names"])

    # Initiate model
    model = Darknet(opt.model_def).to(device)
    model.apply(weights_init_normal)

    # Get dataloader
    dataset = ListDataset(train_path, augment=True)

    dataloader = torch.utils.data.DataLoader(dataset, 
            batch_size=opt.batch_size, 
            shuffle=True,
            collate_fn=dataset.collate_fn
    )

    optimizer = torch.optim.Adam(model.parameters())

    b = len(dataloader)
    min_loss = 1000000
    for epoch in range(opt.epochs):
        model.train()
        print(epoch)
        total_loss = 0
        for batch_i, (_, imgs, targets) in enumerate(tqdm.tqdm(dataloader, desc = "Epoch# " + str(epoch))):
            imgs = Variable(imgs.to(device))
            targets = Variable(targets.to(device), requires_grad=False)
            loss, outputs = model(imgs, targets)
            total_loss += loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        ls = total_loss/b
        # checkpoints 
        if ((ls < min_loss) and (epoch % 10 == 0) and (epoch > 15)):
            min_loss = ls
            file = open("epoch_" + str(epoch) + "_loss.txt","r+")
            file.write(str(min_loss))
            file.close() 
            torch.save(model.state_dict(), "epoch_" + str(epoch) +".pth")