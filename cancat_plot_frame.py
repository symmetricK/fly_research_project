import cv2 # opencv
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
import json
import subprocess
import pdb


path='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/9920211030141500.jpg'


font = cv2.FONT_HERSHEY_SIMPLEX

img1=cv2.imread(path)

text='300sec'
output='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/concat_imgs/test.png'




test_img=cv2.putText(img1,text,(1150,80),font,3,(255,255,255),5)

plot_img='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/trap_2021_10_30_G_200.png'
img2=cv2.imread(plot_img)
shape=np.shape(img1)
row,col=shape[1],shape[0]
res_img2=cv2.resize(img2, dsize=(row,col), interpolation=cv2.INTER_CUBIC)

concat_img=cv2.vconcat([img1,res_img2])

cv2.imwrite(output,concat_img)