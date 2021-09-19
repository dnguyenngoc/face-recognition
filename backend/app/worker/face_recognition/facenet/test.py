import sys
sys.path.insert(0,"../")
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader

import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os
from models import GoogLeNet

from loss_fn import TripletLoss
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
import joblib


PRETRAINED_MODEL="./model_save/best_model.pth"

def load_model():
    model=GoogLeNet()
    model.load_state_dict(torch.load(PRETRAINED_MODEL))
    return model

ARTEFACTS="./artefacts"

def load_artefacts():
    knn=joblib.load(os.path.join(ARTEFACTS,"knn.pkl"))
    return knn

knn=load_artefacts()

pre_model=load_model()
pre_model.cuda()
pre_model.eval()

query_image=np.transpose(np.array(Image.open("./datasets/after_4_bis/1/1.0.jpg")),(2,0,1))/255.0
q_input=torch.tensor(query_image,dtype=torch.float).unsqueeze(0)

q_embedding=pre_model(q_input.cuda()).detach().cpu().numpy()
class_id = knn.predict(q_embedding)
print(class_id[0])
