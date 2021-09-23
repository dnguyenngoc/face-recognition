from os import name
import cv2
import numpy as np
from PIL import Image
from worker.face_detection import FaceDetection
from worker.face_recognition import FaceRecognition


face_detection = FaceDetection()
face_detection.prepare(ctx_id=0, det_size=(640, 640))

face_recognition = FaceRecognition()








