import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import glob
import shutil
import pdb


cropping=False

x_start,y_start,x_end,y_end=0,0,0,0


image_dir = input("Enter a experiment directory you'd like to make a mask: ")
img_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_"+image_dir
data_path=os.path.join(img_dir,'*g')
files=glob.glob(data_path)



img=cv2.imread(files[0])
ori_image=img.copy()

def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event==cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping=True
    # Mouse is Moving
    elif event==cv2.EVENT_MOUSEMOVE:
        if cropping==True:
            x_end, y_end=x, y
    # if the left mouse button was released
    elif event==cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end=x, y
        cropping=False # cropping is finished
        refPoint=[(x_start, y_start), (x_end, y_end)]
        if len(refPoint)==2: #when two points were found
            roi=ori_image[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image",mouse_crop)


while True:
    i=img.copy()
    if not cropping:
        cv2.imshow("image",img)
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
    cv2.waitKey(1)
# close all open windows
cv2.destroyAllWindows()



pdb.set_trace()

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


img2=cv2.imread(files[1])

img2[0:int(y0),:]=1
img2[int(y1):nrows,:]=1
img2[:,0:int(x0)]=1
img2[:,int(x1):ncols]=1


filename2=img_dir+"/mask_check.jpg"
cv2.imwrite(filename2,img2)

print("please, check mask_check.jpg in trap_"+image_dir+" folder in trapcam_timelapse directory")