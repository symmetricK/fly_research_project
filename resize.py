import cv2 # opencv
import numpy as np
import pdb
import matplotlib.pyplot as plt

image_dir_bw="/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_analyzed_videos/trap_2021_10_30_J_videos/20211030_141500_150459_mahal10_trainnum29/annotated_frames/2220211030142437.jpg"
img_bw=cv2.imread(image_dir_bw)
row,col,color=np.shape(img_bw)
cropped_img_bw=img_bw[0:int(row/2),int(col/2)-100:col-100]

image_dir_label="/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_analyzed_videos/trap_2021_10_30_J_videos/20211030_141500_150459_mahal10_trainnum29/annotated_frames/3320211030142437.jpg"
img_label=cv2.imread(image_dir_label)
cropped_img_label=img_label[0:int(row/2),int(col/2)-100:col-100]

image_dir_raw="/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_analyzed_videos/trap_2021_10_30_J_videos/20211030_141500_150459_mahal10_trainnum29/annotated_frames/4420211030142437.jpg"
img_raw=cv2.imread(image_dir_raw)
cropped_img_raw=img_raw[0:int(row/2),int(col/2)-100:col-100]


path="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/"


cv2.imwrite(path+"bw_labeled.jpg",cropped_img_bw)
cv2.imwrite(path+"labeled.jpg",cropped_img_label)
cv2.imwrite(path+"raw.jpg",cropped_img_raw)


pdb.set_trace()

print('test')