import cv2 # opencv
import numpy as np
import pdb
import matplotlib.pyplot as plt

image_dir_bw_nodetection="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/2220211030142437nodetection.jpg"
img_bw_nodetection=cv2.imread(image_dir_bw_nodetection)
row,col,color=np.shape(img_bw_nodetection)
cropped_img_bw_nodetection=img_bw_nodetection[125:int(row/4),int(col/1.75)-100:col-500]

image_dir_bw="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/2220211030142437.jpg"
img_bw=cv2.imread(image_dir_bw)
row,col,color=np.shape(img_bw)
cropped_img_bw=img_bw[125:int(row/4),int(col/1.75)-100:col-500]

image_dir_label="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/3320211030142437.jpg"
img_label=cv2.imread(image_dir_label)
cropped_img_label=img_label[125:int(row/4),int(col/1.75)-100:col-500]

image_dir_raw="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/4420211030142437.jpg"
img_raw=cv2.imread(image_dir_raw)
cropped_img_raw=img_raw[125:int(row/4),int(col/1.75)-100:col-500]


path="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/"

cv2.imwrite(path+"bw.jpg",cropped_img_bw_nodetection)
cv2.imwrite(path+"bw_labeled.jpg",cropped_img_bw)
cv2.imwrite(path+"labeled.jpg",cropped_img_label)
cv2.imwrite(path+"raw.jpg",cropped_img_raw)


added_image = cv2.addWeighted(cropped_img_raw,0.9,cropped_img_bw_nodetection,0.4,0)
cv2.imwrite(path+'combined.png',added_image)


#pdb.set_trace()
