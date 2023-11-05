import argparse
import io
from PIL import Image
import datetime
import torch
import cv2
import numpy as np
import tensorflow as tf
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response 
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess

from subprocess import Popen
import re
import requests
import shutil
import time
import glob

#Just one line to use YOLOv8 in our Flask Application
from ultralytics import YOLO

app=Flask(__name__)

@app.route("/")
def hello_world():#Function to render our Index.html Page
    return render_template('index.html")


@app.route("/",methods=["GET","POST"])
def predict_img():
    if(request.method == "POST"):
        if(file in request.files):
            f=request.files['file']#Reading the Data given to HTML File
            #Fetching the File when user clicks upload
            basepath=os.path.dirname(__file__)
            filepath=os.path.join(basepath,'uploads',f.filename)
            print("Upload folder is ",filepath)
            f.save(filepath)
            global imgpath
            predict_img.imgpath=f.filename
            print("Printing predict img -",predict_img)

            file_extension=f.filename.rsplit('.', 1) [1].lower()

            if(file extension=="jpg"):
                img=cv2.imread(filepath)
                frame=cv2.imencode(".jpg",cv2.UMat(img))[1].tobytes()
                Image=Image.open(io.BytesIO(frame))

                #Performing the Detection
                yolo=YOLO("best.pt")
                detections=yolo.predict(image,save=True)
                return display(f.filename)

#The display function is used to serve the image or video from the folder path directory
@app.route('/<path:filename>')
def display(filename):
    folder_path="runs/detect"
    subfolders=[f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path,f))]
    latest_subfolder=max(subfolders,key=lambda x:os.path.getctime(os.path.join(folder_path,x)))
    directory=folder_path+'/'+latest_subfolder
    print("Printing directory- ",directory)
    files=os.listdir(directory)
    latest_file=files[0]

    print(latest_file)
    filename=os.path.join(folder_path,latest_subfolder,latest_file)
    file_extension=filename.rsplit('.', 1) [1].lower()
    environ=request.environ
    if(file_extension=="jpg"):
        return (send from directory(directory,latest file,environ)) #Shows the result in seperate tab
    else:   
        return "Invalid file format"

if __name__=="__main__":
    pass