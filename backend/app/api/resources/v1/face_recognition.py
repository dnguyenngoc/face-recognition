"""
@ Duy Nguyen
"""

from fastapi import APIRouter


router = APIRouter()


@router.post("/predict")
def face_recognition():
    pass