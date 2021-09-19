"""
@ Duy Nguyen
"""

from fastapi import APIRouter
from worker.ml import face_detection
import cv2
import numpy as np
from PIL import Image

router = APIRouter()


@router.post("/detection")
def face_detection_test():
    image = cv2.imread('./worker/insightface/data/images/t1.jpg')
    faces = face_detection.get(image)
    for i in range(len(faces)):
        face = faces[i].bbox.astype(np.int)
        crop = face_detection.crop_image(image, face)
        im = Image.fromarray(np.uint8(crop)).convert('RGB')
        im = im.resize((224,224))
        im.save('./api/resources/v1/{}.jpg'.format(i))