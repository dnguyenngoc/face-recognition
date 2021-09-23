import cv2
import numpy as np
from PIL import Image
from worker.face_detection import FaceDetection


face_detection = FaceDetection()
face_detection.prepare(ctx_id=0, det_size=(640, 640))


import glob


paths = glob.glob("./datasets/tet/**/*")
i = 0
for path in paths: 
    name = path.split('\\')[-2]
    file_old = path.split('\\')[-1]
    print(name)
    image = cv2.imread(path)
    faces = face_detection.get(image)
    print('==============================================', name)
    if name in ['heo', 'pot', 'cherry', 'ruby','hai', 'le']:
        continue
    for face in faces:
        try:
            face = face.bbox.astype(np.int)
            crop = face_detection.crop_image(image, face)
            im = Image.fromarray(np.uint8(crop)).convert('RGB')
            im = im.resize((160,160))
            im.save("./datasets/family/" + name + '_' +  file_old[0:5] + '_' + str(i) + '.jpg')
            i+= 1
        except:
            print(path)
            i+= 1
            continue
    print('==============================================')
