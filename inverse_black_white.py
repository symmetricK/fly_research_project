import numpy as np
import cv2
import matplotlib.pyplot as plt
import pdb

original_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/contour_frame.jpg"
img=cv2.imread(original_dir)
img2=np.invert(img)

filename="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/contour_frame_inverted.jpg"
cv2.imwrite(filename,img2)
