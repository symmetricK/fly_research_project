import cv2 # opencv
import numpy as np
import pdb
import matplotlib.pyplot as plt
import os
import glob

# to get row and col
image_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/220317_WT_80frames/14-02-12.477627.jpg"
image=cv2.imread(image_dir)
row,col,color=np.shape(image)

# to read through one folder
path="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/220317_WT_80frames"
data_path=os.path.join(path,'*g')
files=glob.glob(data_path)
sorted_files=sorted(files)


# they are none type of objects
path1="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/220317_WT_80frames/cropped_80frames_jpg/"
path2="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/220317_WT_80frames/cropped_80frames_png/"

count=1
for file in sorted_files:
	img=cv2.imread(file)
	cropped_img=img[int(row/2)+300:int(row*3/4)+200,int(col/2)+100:int(col*3/4)-150]
#	pdb.set_trace()
	if count<10:
		cv2.imwrite(path1+"00"+str(count)+".jpg",cropped_img)
		cv2.imwrite(path2+"00"+str(count)+".png",cropped_img)
	else:
		cv2.imwrite(path1+"0"+str(count)+".jpg",cropped_img)
		cv2.imwrite(path2+"0"+str(count)+".png",cropped_img)		
	count=count+1



# to conevert pngs to mp4 file

#ffmpeg -r 10 -pattern_type glob -i '*.png' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4



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


