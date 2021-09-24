"""
@ Duy Nguyen
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from worker.ml import face_detection
from PIL import Image, ImageDraw
from helpers import image as image_helper
import uuid
from glob import glob
import os
from settings import config
import numpy as np

router = APIRouter()


@router.post("/crop-face")
def face_detection_test(
    image: UploadFile = File(...),
):
    image = image.file.read()
    image_det = image_helper.io_bytes_to_numpy(image)
    # im_reg = cv2.cvtColor(image_det, cv2.COLOR_BGR2RGB)
    im_reg = Image.fromarray(image_det)

    faces = face_detection.get(image_det)
    name_file = str(uuid.uuid4().hex) + '.jpg'
    list_file = []
    for face in faces:
        face = face.bbox.astype(np.int)
        crop_image = face_detection.crop_image(image_det, face)
        im = Image.fromarray(np.uint8(crop_image))
        im.save(config.FACE_DETECTION_DIR + name_file)
        list_file.append('http://localhost:8081/api/v1/images/show/{}/{}'.format(config.FACE_DETECTION_DIR.split("/")[-2],name_file))
    return list_file
