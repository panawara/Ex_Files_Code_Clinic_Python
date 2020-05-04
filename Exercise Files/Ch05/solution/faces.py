#!/usr/bin/python3
""" Facial Detection by Barron Stone for Code Clinic: Python """
import os
import cv2
import imageio
import json
import tkinter as tk
from tkinter import filedialog

def detectFaces(img_path, display=False):
    try:
        if img_path.lower().endswith('.png'):
            color_img = cv2.imread(img_path)
        elif img_path.lower().endswith(('.jpg','.jpeg')):
            color_img = cv2.imread(img_path)
        elif img_path.lower().endswith('.gif'):
            color_img = imageio.mimread(img_path)[0] # first frame of gif
            color_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)
    except Exception as e:
        raise e

    # scale image to fit within 1280x720
    h = color_img.shape[0] # image height
    w = color_img.shape[1] # image width
    if (w/h) > (1280/720): # scale based on width
        color_img = cv2.resize(color_img, (1280, int(h*1280/w)))
    else: # scale based on height
        color_img = cv2.resize(color_img, (int(w*720/h), 720))

    # convert to grayscale images
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY).copy()

    # load Haar cascade and detect faces
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    faces = cascade.detectMultiScale(gray_img)
    print('Found {0} face{1} in {2}'.format(len(faces),'s' if (len(faces) > 1) else '', os.path.basename(img_path)))

    if display:
        # draw rectangles on faces
        for (x, y, w, h) in faces:
            cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # display image with OpenCV
        cv2.imshow('Facial Detection', color_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return json.dumps({'countFaces': len(faces),
                       'imageLocation': img_path})

def main():
    # open file dialog to choose input image
    root = tk.Tk()
    root.withdraw()
    img_path = filedialog.askopenfilename(initialdir = './photos',
                                          title = 'Choose an Image to Analyze',
                                          filetypes = (('JPEG','*.jpg;*.jpeg'),
                                                       ('GIF','*.gif'),
                                                       ('PNG','*.png'),
                                                       ('all files','*.*')))
    output = detectFaces(img_path, display=True)
    json_path = ('.').join(img_path.split('.')[:-1]) + '.json'
    x = input('Save result to {}? [y/n]: '.format(os.path.basename(json_path)))
    if x.lower() in ('y','ye','yes'):
        f = open(json_path, 'w')
        f.write(output)
        f.close()
        print('Saved result to {}!'.format(os.path.basename(json_path)))

if __name__ == "__main__": main()
