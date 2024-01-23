# -*- coding: utf-8 -*-


import cv2
import glob
video_array=[]
path=r"C:\Users\hughd\Desktop\final year project\new video"
files=glob.glob(path + '\*.jpeg')
files.sort()
for filename in files:
    #looping through the images
    new_img=cv2.imread(filename)
    video_array.append(new_img)
    #reading the images
    height,width,layers=new_img.shape
    size=(width,height)
    out=cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'),15,size)
    for i in range(len(video_array)):
        out.write(video_array[i])
    out.release()
    #appends images to array
    
    
    
    
    
    
    
    
    