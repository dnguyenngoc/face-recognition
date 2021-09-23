from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np


def read_from_url(url: str):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def read_from_path(path: str):
    image= cv2.imread(path)
    return image


def io_bytes_to_numpy(io_bytes):
    image = Image.open(BytesIO(io_bytes))
    return  np.asarray(image)
