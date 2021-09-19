"""
Final of Ml model load with fastapi
"""

import onnxruntime
from worker.insightface.utils import ensure_available
from worker.insightface import model_zoo
from worker import ml_config
import glob
import os.path as osp
from worker.insightface.app.common import Face
import numpy as np


class FaceDetection():
    def __init__(
        self, 
        name: str = ml_config.MODEL_NAME_DEFAULT, 
        root: str = ml_config.MODEL_DIR_PATH, 
        allowed_modules=None,
        **kwargs
    ):
        onnxruntime.set_default_logger_severity(3)
        self.models = None
        self.model_dir = ensure_available('models', name, root=root)
        onnx_files = glob.glob(osp.join(self.model_dir, '*.onnx'))
        onnx_file = onnx_files[0]
        self.model = model_zoo.get_model(onnx_file, **kwargs)
      

    def prepare(self, ctx_id, det_thresh=0.5, det_size=(640, 640)):
        self.det_thresh = det_thresh
        assert det_size is not None
        print('set det-size:', det_size)
        self.det_size = det_size
        self.model.prepare(ctx_id, input_size=det_size, det_thresh=det_thresh)


    def get(self, img, max_num=0):
        bboxes, kpss = self.model.detect(img,
                                             max_num=max_num,
                                             metric='default')
        if bboxes.shape[0] == 0:
            return []
        ret = []
        for i in range(bboxes.shape[0]):
            bbox = bboxes[i, 0:4]
            det_score = bboxes[i, 4]
            kps = None
            if kpss is not None:
                kps = kpss[i]
            face = Face(bbox=bbox, kps=kps, det_score=det_score)
            ret.append(face)
        return ret

    def draw_on(self, img, faces):
        import cv2
        dimg = img.copy()
        for i in range(len(faces)):
            face = faces[i]
            box = face.bbox.astype(np.int)
            color = (0, 0, 255)
            cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
            if face.kps is not None:
                kps = face.kps.astype(np.int)
                for l in range(kps.shape[0]):
                    color = (0, 0, 255)
                    if l == 0 or l == 3:
                        color = (0, 255, 0)
                    cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color,
                               2)
            if face.gender is not None and face.age is not None:
                cv2.putText(dimg,'%s,%d'%(face.sex,face.age), (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
        return dimg


    def crop_image(self, image, bbox):
        crop = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        return crop
