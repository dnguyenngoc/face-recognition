from os import name
import cv2
import numpy as np
from face_recognition.insightface.app import FaceAnalysis
from face_recognition.insightface.data import get_image as ins_get_image
from face_recognition.insightface import model_zoo

check_age = FaceAnalysis()
check_age.prepare(ctx_id=0, det_size=(640, 640))
