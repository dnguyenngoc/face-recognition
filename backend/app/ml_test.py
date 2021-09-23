import cv2
import numpy as np
from PIL import Image
from worker.facenet_recognition.draw_func import draw_box
from worker.face_detection import FaceDetection
from worker.face_recognition import FaceRecognition

face_detection = FaceDetection()
face_detection.prepare(ctx_id=0, det_size=(640, 640))

face_recognition = FaceRecognition()

image_det = cv2.imread('./worker/data_test/t1.jpg')
print("[Det Image]", type(image_det))
im_reg = cv2.cvtColor(image_det, cv2.COLOR_BGR2RGB)
im_reg = Image.fromarray(im_reg)
print("[Reg Image]", type(im_reg))

from PIL import ImageDraw
import matplotlib.pyplot as plt

faces = face_detection.get(image_det)

boxes, probs, kps =  [], [], []
for face in faces:
    boxes.append(face['bbox'])
    probs.append(face['det_score'])
    kps.append(face['kps'])
print("DETECTION: ", boxes, probs)
idx, prob = face_recognition.recogniton(im_reg, boxes)


classes = {'a. Trãi': 0, 'a. Tuấn': 1, 'a. Tú': 2, 'c. Manh': 3, 'c. Ánh': 4, 'cherry': 5, 'chuột': 6, 'con Dương =))': 7, 'hai': 8, 'heo': 9, 'le': 10, 'loi': 11, 'mami': 12, 'o úc': 13, 'papa': 14, 'pot': 15, 'ruby': 16, 'sộ': 17, 'undefined': 18}

classes_new = {}
for key, value in classes.items():
    classes_new[value] = key

idx = [classes_new[ix] for ix in idx]

draw = ImageDraw.Draw(im_reg)

boxes, probs = draw_box(draw, boxes, idx, probs, 0.87)
print(boxes, probs)

im_reg.show()