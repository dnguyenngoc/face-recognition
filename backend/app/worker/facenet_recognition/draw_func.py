import numpy as np
from PIL import ImageFont, ImageDraw
import os
from worker import ml_config


def diag(x1, y1, x2, y2):
    return np.linalg.norm([x2 - x1, y2 - y1])


def square(x1, y1, x2, y2):
    return abs(x2 - x1) * abs(y2 - y1)


def isOverlap(rect1, rect2):
    x1, x2 = rect1[0], rect1[2]
    y1, y2 = rect1[1], rect1[3]

    x1_, x2_ = rect2[0], rect2[2]
    y1_, y2_ = rect2[1], rect2[3]

    if x1 > x2_ or x2 < x1_: return False 
    if y1 > y2_ or y2 < y1_: return False
  
    rght, lft = x1 < x1_ < x2, x1_ < x1 < x2_
    d1, d2 = 0, diag(x1_, y1_, x2_, y2_)
    threshold = 0.5

    if rght and y1 < y1_: d1 = diag(x1_, y1_, x2, y2)
    elif rght and y1 > y1_: d1 = diag(x1_, y2_, x2, y1)
    elif lft and y1 < y1_: d1 = diag(x2_, y1_, x1, y2) 
    elif lft and y1 > y1_: d1 = diag(x2_, y2_, x1, y1)

    if d1 / d2 >= threshold and square(x1, y1, x2, y2) < square(x1_, y1_, x2_, y2_): return True
    return False

def draw_box(draw, boxes, names, probs, min_p=0.89):
    font = ImageFont.truetype(os.path.join(ml_config.FONT_PATH , 'arial.ttf'), size=13)

    not_overlap_inds = []
    for i in range(len(boxes)): 
        not_overlap = True
        for box2 in boxes: 
            if np.all(boxes[i] == box2): continue 
            not_overlap = not isOverlap(boxes[i], box2)   
            if not not_overlap: break 
        if not_overlap: not_overlap_inds.append(i)

    boxes = [boxes[i] for i in not_overlap_inds] 
    probs = [probs[i] for i in not_overlap_inds]
    for box, name, prob in zip(boxes, names, probs):
        if prob >= min_p: 
            if name == 'pot': color = 'yellow'
            else: color = 'white'
            draw.rectangle(box.tolist(), outline=(255, 255, 255), width=3,)
            x1, y1, _, _ = box
            text_width, text_height = font.getsize(f'{name}')
            draw.rectangle(((x1, y1 - text_height), (x1 + text_width, y1)), fill=color)
            draw.text((x1, y1 - text_height), f'{name}', (24, 12, 30), font) 
            # draw.text((x1, y1 - text_height), f'{name}: {prob:.2f}', (24, 12, 30), font) 
        else:
            name = 'chịu'
            draw.rectangle(box.tolist(), outline=(255, 255, 255), width=3)
            x1, y1, _, _ = box
            text_width, text_height = font.getsize(f'{name}')
            draw.rectangle(((x1, y1 - text_height), (x1 + text_width, y1)), fill='white')
            draw.text((x1, y1 - text_height), f'{name}', (24, 12, 30), font) 
            # draw.text((x1, y1 - text_height), f'{name}: {prob:.2f}', (24, 12, 30), font) 
    return boxes, probs 