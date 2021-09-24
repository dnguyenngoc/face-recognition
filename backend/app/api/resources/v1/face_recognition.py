"""
@ Duy Nguyen
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from worker.ml import face_detection, face_recognition, classes_new
from PIL import Image, ImageDraw
from helpers import image as image_helper
from worker.facenet_recognition.draw_func import draw_box
import uuid
from glob import glob
import os
from settings import config

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

    boxes, probs = draw_box(draw, boxes, idx, probs, 0.84)

    name_file = str(uuid.uuid4().hex) + '.jpg'

    im_reg.save('{}{}'.format(config.FACE_RECOGNITION_DIR, name_file))

    return "http://localhost:8081/api/v1/images/show/{}/{}".format(config.FACE_RECOGNITION_DIR.split("/")[-2], name_file)


@router.post("/remove-tmp")
def remove(type: str = 'recognition'): 
    if type == 'recognition':
        paths = glob('{}*.jpg'.format(config.FACE_RECOGNITION_DIR))
    elif type == 'detection':
        paths = glob('{}*.jpg'.format(config.FACE_DETECTION_DIR))
    else: raise HTTPException(400, 'not support this type!')
    for item in paths:
        try: os.remove(item)
        except: continue
    return paths