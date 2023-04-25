import sys
from time import sleep

import cv2
import pyocr
import pyautogui as py
from PIL import Image

sleep(1)

ocr_engines = pyocr.get_available_tools()
ocr_engine = ocr_engines[0]

def similar_rate(previous,new):
    pass

cap = cv2.VideoCapture(0)
# setting for sfc typing test
x = 95
y = 265
w = 840
h = 210

# setting for 日本語タイピング
x = 150
y = 530
w = 700
h = 30

previous_sentence = ""
snaped = False
while True:
    ret, frame = cap.read()
    frame = frame[y:y+h, x:x+w]
    if not snaped:
    cv2.imwrite("test.jpg", frame)
    pil_frame = Image.fromarray(frame)
    txt = ocr_engine.image_to_string(pil_frame, lang="eng")
    print(txt)
    txt = txt.replace("\n", " ")
    if txt == "FINISH!":
        break
    py.write(txt)
    sleep(0.2)
    """
    cv2.imshow("", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    """
