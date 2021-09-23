import joblib
import torch
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from facenet_pytorch import fixed_image_standardization
import numpy as np
from worker import ml_config

standard_transform = transforms.Compose([
                                transforms.Resize((160, 160)),
                                np.float32, 
                                transforms.ToTensor(),
                                fixed_image_standardization
])


class FaceRecognition(object):
    def __init__(self, model_path: str = ml_config.REG_MODEL_PATH) -> None:
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print(f'Running on device: {self.device}')
        self.ebb_model = InceptionResnetV1(pretrained='vggface2', dropout_prob=0.6, device=self.device).eval()
        self.model = joblib.load(model_path)
        self.ebb_model.eval()


    def get_embedding(self, image, boxes):
        x = torch.stack([standard_transform(image.crop(b)) for b in boxes])
        embeds = self.ebb_model(x.to(self.device))
        embeds = embeds.detach().cpu().numpy()
        return embeds

    def recogniton(self, image, boxes):
        names, probs = [], []
        if len(boxes):
            embeds = self.get_embedding(image, boxes)
            idx, prob = self.model.predict(embeds), self.model.predict_proba(embeds).max(axis=1)
            print(idx, prob)
        return(idx, prob)
