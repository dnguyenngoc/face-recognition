from os import name
import cv2
import numpy as np
from PIL import Image
from worker.face_detection import FaceDetection
from worker.face_recognition import FaceRecognition


face_detection = FaceDetection()
face_detection.prepare(ctx_id=0, det_size=(640, 640))

face_recognition = FaceRecognition()

classes = {'a. Trãi': 0, 'a. Tuấn': 1, 'a. Tú': 2, 'c. Manh': 3, 'c. Ánh': 4, 'cherry': 5, 'chuột': 6, 'con Dương =))': 7, 'hai': 8, 'heo': 9, 'le': 10, 'loi': 11, 'mami': 12, 'o úc': 13, 'papa': 14, 'pot': 15, 'ruby': 16, 'sộ': 17, 'undefined': 18}

classes_new = {}
for key, value in classes.items():
    classes_new[value] = key








