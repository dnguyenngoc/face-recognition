"""
@ Duy Nguyen
"""

from fastapi import APIRouter, UploadFile, File
from worker.ml import face_detection, face_recognition, classes_new
import numpy as np
from PIL import Image, ImageDraw
from helpers import image as image_helper
import cv2
from worker.facenet_recognition.draw_func import draw_box
import uuid


router = APIRouter()


@router.post("/recognition")
def face_detection_test(
    image: UploadFile = File(...),
):
    image = image.file.read()
    image_det = image_helper.io_bytes_to_numpy(image)
    # im_reg = cv2.cvtColor(image_det, cv2.COLOR_BGR2RGB)
    im_reg = Image.fromarray(image_det)

    faces = face_detection.get(image_det)
    boxes, probs, kps =  [], [], []
    
    for face in faces:
        boxes.append(face['bbox'])
        probs.append(face['det_score'])
        kps.append(face['kps'])
    idx, prob = face_recognition.recogniton(im_reg, boxes)

    idx = [classes_new[ix] for ix in idx]

    draw = ImageDraw.Draw(im_reg)

    boxes, probs = draw_box(draw, boxes, idx, probs, 0.86)

    name_file = str(uuid.uuid4().hex) + '.png'

    im_reg.save('./api/resources/v1/tmp/{}'.format(name_file))

    return {
        "url": "https://localhost:8081/api/v1/image/show/{}".format(name_file)
    }