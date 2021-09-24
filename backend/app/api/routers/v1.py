from fastapi import APIRouter

from api.resources.v1 import account, face_recognition, images, face_detection, video


router = APIRouter()


router.include_router(account.router, prefix="/account",  tags=["V1-Account"])
router.include_router(face_recognition.router, prefix="/face-recogniton",  tags=["V1-Face"])
router.include_router(face_detection.router, prefix="/face-detection",  tags=["V1-DET"])
router.include_router(images.router, prefix="/images",  tags=["V1-Images"])
router.include_router(video.router, prefix="/video",  tags=["V1-Video"])


