import cv2 # opencv
import numpy as np
import pdb
import matplotlib.pyplot as plt
import os
import glob

# to get row and col
image_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/40frames/14-02-35.980501.jpg"
image=cv2.imread(image_dir)
row,col,color=np.shape(image)

# to read through one folder
path="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/40frames"
data_path=os.path.join(path,'*g')
files=glob.glob(data_path)
sorted_files=sorted(files)


# cropped images for jpg
path1="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/cropped_40frames_jpg/"
path2="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/cropped_40frames_png/"

count=1
for file in sorted_files:
	img=cv2.imread(file)
	cropped_img=img[int(row/2)+300:int(row*3/4)+200,int(col/2)+100:int(col*3/4)-150]
	cv2.imwrite(path1+str(count)+".jpg",cropped_img)
	cv2.imwrite(path2+str(count)+".png",cropped_img)
	count=count+1

# read all jpgs
#data_path1=os.path.join(path1,'*g')
#jpgs=glob.glob(data_path1)
#sorted_jpgs=sorted(jpgs)

#pdb.set_trace()
 
#path2="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/cropped_40frames_png/"

#c=1
#for i in sorted_jpgs:
#	plt.imread(i)
#	pdb.set_trace()
#	c=c+1
#	plt.close()


