import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
import shutil

img_dir="/home/flyranch/2017_10_26_trap_G_raw_data_sample"
data_path=os.path.join(img_dir,'*g')
files=glob.glob(data_path)

data=[]
for file in files:
    img=cv2.imread(file)
    data.append(img)

data_array=np.asarray(data)
med=np.median(data_array,axis=0)
int_med=med.astype(int)

count=0

while(count<10):
	filename='/home/flyranch/field_data_and_analysis_scripts/2017_10_26/trapcam_timelapse/trap_G/tl_0006_000'+str(count)+'_20161130_00000'+str(count)+'.jpg'
	cv2.imwrite(filename,int_med)
	count=count+1