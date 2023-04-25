import os
import sys
from time import sleep

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

import cv2
import pyocr
import numpy as np
import pyautogui as py
from PIL import Image

def show(img):
    cv2.imshow("",img)
    cv2.waitKey(0)

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # window setting
        self.win_width = 1200
        self.win_height = 900
        self.master.geometry("{}x{}".format(self.win_width, self.win_height))

        ocr_engines = pyocr.get_available_tools()
        self.ocr_engine = ocr_engines[0]

        # canvas setting
        self.canvas = tk.Canvas(self.master)
        self.canvas_width = 1200
        self.canvas_height = 800
        self.canvas.configure(width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # clip setting
        self.first_position = []
        self.second_position = []
        self.clicked = False

        # capture
        self.capture = py.screenshot()
        self.original_image_width, self.original_image_height = self.capture.size
        #print(self.capture.size)
        # aspect ratio
        aspect_width, aspect_height = self.get_aspect_ratio(self.capture)
        #print("aspect", aspect_width, aspect_height)
        # resize image
        self.canvas_image_height = self.canvas_height
        self.canvas_image_width = int( (aspect_width * self.canvas_image_height) / aspect_height )
        #print(self.canvas_image_width, self.canvas_image_height)
        self.canvas_image = self.capture.resize((self.canvas_image_width, self.canvas_image_height))
        self.tk_img = ImageTk.PhotoImage(self.canvas_image)

        self.canvas.bind("<Button-1>", self.first_click)
        self.canvas.bind("<ButtonRelease-1>", self.second_click)
        self.canvas.bind("<Motion>", self.rect)
        self.master.bind("<Key-s>", self.start)

        self.show()


    def get_aspect_ratio(self, image):
        image_width, image_height = image.size
        max_divisor = self.gcd(image_width, image_height)
        aspect_width = int(image_width / max_divisor)
        aspect_height = int(image_height / max_divisor)
        return aspect_width, aspect_height

    def start(self, event):
        print("Start in 2 sec")
        sleep(2)
        py.write(self.txt)


    def detect_txt(self, image):
        txt = self.ocr_engine.image_to_string(image, lang="eng")
        return txt

    def rect(self, event):
        #print("debug")
        if self.clicked:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)
            current_mouse_x = event.x
            current_mouse_y = event.y
            first_x = self.first_position[0]
            first_y = self.first_position[1]
            #print(first_x, first_y)
            #print(current_mouse_x, current_mouse_y)
            self.canvas.create_rectangle(first_x, first_y, event.x, event.y, width=3)

    def clip(self):
        # only call from second_position()
        ratio = self.original_image_height / self.canvas_image_height
        first_x = self.first_position[0] * ratio
        first_y = self.first_position[1] * ratio
        second_x = self.second_position[0] * ratio
        second_y = self.second_position[1] * ratio
        #print(first_x, first_y)
        #print(second_x, second_y)
        # アスペクト比の補正
        w = abs(second_x - first_x)
        h = abs(second_y - first_y)
        self.clip_img = self.capture.crop((first_x, first_y, first_x+w, first_y+h))
        self.txt = self.detect_txt(self.clip_img)
        #print(txt)
        #self.clip_img.save("clip.png")

    def first_click(self, event):
        self.first_position = []
        self.first_position.append(event.x)
        self.first_position.append(event.y)
        self.clicked = True

    def second_click(self, event):
        self.second_position = []
        self.second_position.append(event.x)
        self.second_position.append(event.y)
        self.clip()
        self.clicked = False
        
    def gcd(self, x, y):
        if (y == 0):
            return x
        return self.gcd(y, x % y)
    
    def show(self):
        self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
