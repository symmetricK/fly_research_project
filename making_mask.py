import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
import shutil
import pdb


image_dir = input("Enter a directory name (without trap_) you'd like to create a mask: ")
date=input("Enter what date did you do this experiment (e.g. 20220725): ")
img_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/"+date+"/trap_"+image_dir
data_path=os.path.join(img_dir,'*g')
files=glob.glob(data_path)

#data=[]
#for file in files:
#    img=cv2.imread(file)
#    data.append(img)

#data_array=np.asarray(data)
#med=np.median(data_array,axis=0)
#int_med=med.astype(int)
#pdb.set_trace()
#filename=img_dir+"/mask.jpg"


img=cv2.imread(files[0])
[nrows,ncols,colors]=np.shape(img)
mask=np.int8(np.zeros((nrows,ncols)))

print("Decide the region of mask you want to focus on,")

x0=input("x0:")
x1=input("x1:")
y0=input("y0:")
y1=input("y1:")
#pdb.set_trace()
mask[int(y0):int(y1),int(x0):int(x1)]=1
filename=img_dir+"/mask.jpg"
cv2.imwrite(filename,mask)

print("mask.jpg created")


img2=cv2.imread(files[-500])

img2[0:int(y0),:]=1
img2[int(y1):nrows,:]=1
img2[:,0:int(x0)]=1
img2[:,int(x1):ncols]=1


filename2=img_dir+"/mask_check.jpg"
cv2.imwrite(filename2,img2)


#pdb.set_trace()

print("please, check mask_check.jpg in trap_"+image_dir+" folder in trapcam_timelapse/"+date+" directory")