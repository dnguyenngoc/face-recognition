import cv2
import numpy as np
from PIL import Image
from worker.facenet_recognition.draw_func import draw_box
from worker.face_detection import FaceDetection
from worker.face_recognition import FaceRecognition

face_detection = FaceDetection()
face_detection.prepare(ctx_id=0, det_size=(640, 640))

face_recognition = FaceRecognition()

image_det = cv2.imread('./worker/data_test/20190810_192549.jpg')
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



classes = {1: "Pot", 2: "Đông Anh", 3: "Rupy"}
idx = [classes[ix] for ix in idx]

draw = ImageDraw.Draw(im_reg)

boxes, probs = draw_box(draw, boxes, idx, probs, 0.7)
print(boxes, probs)

im_reg.show()