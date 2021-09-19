from glob import glob
import config_train as config
import pandas as pd

from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

le = preprocessing.LabelEncoder()


import torch
from models import GoogLeNet
import numpy as np
from PIL import Image


PRETRAINED_MODEL="./model_save/best_model.pth"
def load_model():
    model=GoogLeNet()
    model.load_state_dict(torch.load(PRETRAINED_MODEL))
    return model
pre_model=load_model()
pre_model.cuda()
pre_model.eval()


# def load_df():
#     paths=glob(config.IMG_PATH)
#     labels=[path.split("\\")[-2] for path in paths]
#     file_name=[path.split("\\")[-1] for path in paths]
#     df=pd.DataFrame({"img_paths":paths,"labels":labels,"file_name":file_name})
#     df["img_paths"]=df["img_paths"].apply(lambda x: x.replace("\\","/"))
#     return df

def load_df():
    paths=glob(config.IMG_PATH)
    labels=[path.split("\\")[-1][:-4].split(".")[0] for path in paths]
    file_name=[path.split("\\")[-1][:-4].split(".")[1] for path in paths]
    df=pd.DataFrame({"img_paths":paths,"labels":labels,"file_name":file_name})
    df["img_paths"]=df["img_paths"].apply(lambda x: x.replace("\\","/"))
    return df#.head(500)


df = load_df()
lable_encoded = le.fit_transform(df['labels'])

image_encodes = []
for item in df['img_paths']:
    query_image=np.transpose(np.array(Image.open(item)),(2,0,1))/255.0
    q_input=torch.tensor(query_image,dtype=torch.float).unsqueeze(0)
    q_embedding=pre_model(q_input.cuda()).detach().cpu().numpy()[0]
    image_encodes.append(q_embedding)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(image_encodes, lable_encoded, test_size=0.3)


knn = KNeighborsClassifier(n_neighbors=1426)

knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

from sklearn import metrics

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

import pickle
filename = './artefacts/knn.pkl'
pickle.dump(knn, open(filename, 'wb'))
 
# some time later...
 
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.predict([image_encodes[6]])
print(result[0] + 1)
print(df['img_paths'][5])