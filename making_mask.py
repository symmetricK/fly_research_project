import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
import shutil
import pdb


image_dir = input("Enter the experiment directory you'd like to make a mask: ")
img_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_"+image_dir
data_path=os.path.join(img_dir,'*g')
files=glob.glob(data_path)

data=[]
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
mask=np.int8(np.ones((nrows,ncols)))

filename=img_dir+"/mask.jpg"

print("created mask.jpg")
#cv2.imwrite(filename,int_med)
cv2.imwrite(filename,mask)