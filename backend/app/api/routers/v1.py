from fastapi import APIRouter

from api.resources.v1 import account, face_recognition, images

router = APIRouter()


router.include_router(account.router, prefix="/account",  tags=["V1-Account"])
router.include_router(face_recognition.router, prefix="/face-recogniton",  tags=["V1-Face"])
router.include_router(images.router, prefix="/images",  tags=["V1-Images"])

