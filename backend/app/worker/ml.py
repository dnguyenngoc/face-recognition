from os import name
import cv2
import numpy as np
from face_recognition.insightface.app import FaceAnalysis
# from face_recognition.insightface.data import get_image as ins_get_image
# from face_recognition.insightface import model_zoo
from PIL import Image


face_age = FaceAnalysis()
face_age.prepare(ctx_id=0, det_size=(640, 640))


import glob

for i in range(3):
    number = i+1
    paths = glob.glob("./face_recognition/facenet/datasets/family_origin/{}/*".format(number))

    for path in paths:
        image = cv2.imread(path)
        faces = face_age.get(image)
        face = faces[0].bbox.astype(np.int)
        crop = face_age.crop_image(image, face)
        im = Image.fromarray(np.uint8(crop)).convert('RGB')
        im = im.resize((224,224))
        im.save("./face_recognition/facenet/datasets/family/{}/{}".format(number, path.split("\\")[-1].lower().replace('jpeg', 'jpg').replace('png', 'jpg')))
