# rasberrypi-ai

## Model
https://drive.google.com/drive/u/0/folders/1BeOpAg2Y5XFaOdrI4oz6I47ux3c8GQvf

`contact with admin to get model`

## How to run?

### 1. copy docker-compose.prod.yaml

https://github.com/apot-group/rasberrypi-ai/docker-compose.prod.yaml


### 2. dowload model fro model link   
`contact with admin to get model`

### 3 Change path file to of docker-compose.prod.yaml to your model file
```
  - {path-to-env-file}:/app/env-staging.ini
  - {path-to-fact-detection-model-file}:/app/worker/insightface/save_model/models/face_detection/scrfd_10g_bnkps.onnx
  - {path-to-fact-recognition-label-file}:/app/worker/facenet_recognition/save_model/classes_label.json
  - {path-to-fact-recognition-model-file}:/app/worker/facenet_recognition/save_model/svm.sav
  
  # EX FOR ME
  # - ./backend/app/env-staging.ini:/app/env-staging.ini
  # - ./backend/app/worker/insightface/save_model/models/face_detection/scrfd_10g_bnkps.onnx:/app/worker/insightface/save_model/models/face_detection/scrfd_10g_bnkps.onnx
  # - ./backend/app/worker/facenet_recognition/save_model/classes_label.json:/app/worker/facenet_recognition/save_model/classes_label.json
  # - ./backend/app/worker/facenet_recognition/save_model/svm.sav:/app/worker/facenet_recognition/save_model/svm.sav
```

### 4. start with docker-compose
```
docker-compose -f docker-compose.prod.yaml -up
```

## FOR DEV

### 1. Install docker and docker-compose:

https://www.docker.com/

### 2. Clone this repo
`git clone https://github.com/apot-group/rasberrypi-ai.git` 

### 2. Download model from Model link
`contact with admin to get permission` 

### 3. From project dir:

`docker-compose up`

## API DOCS

Api docs at: http://localhost:8081/api/docs#/ or http://localhost:8081/api/redoc#/


<!-- <div align="center">
    <img src="./docs/server.png">
</div>
<br /> 
<br />  -->

<!--follow intagram or CONTACT to me if you have any question? -->

Contact
=======
Email: duynguyenngoc@hotmail.com