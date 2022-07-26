import cv2 # opencv
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
import json
import pdb
from time import strftime
from datetime import datetime

# Create point matrix get coordinates of mouse click on image
#point_matrix = np.zeros((1000,1000),np.int)

counter = 0
def mousePoints(event,x,y,flags,params):
    global counter
    # Left button mouse click event opencv
    if event==cv2.EVENT_LBUTTONDOWN:
        #point_matrix[counter] = x,y
        counter=counter+1
    	print(counter)
    	cv2.circle(img,(x,y),3,(0,255,0),cv2.FILLED)


# Read image
img = cv2.imread('/home/flyranch/Desktop/Oct_5520211030142132.jpg')
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
# displaying the image
cv2.imshow('image', img)

cv2.setMouseCallback("image", mousePoints)

while True:
	if cv2.waitKey(1)==ord('q'):
		break
	if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE)<1:
		break
	# close the window
cv2.destroyAllWindows()


#while True:
#    for x in range (0,2):
#        cv2.circle(img,(point_matrix[x][0],point_matrix[x][1]),3,(0,255,0),cv2.FILLED)
 
#    if counter == 2:
#        starting_x = point_matrix[0][0]
#        starting_y = point_matrix[0][1]
# 
#        ending_x = point_matrix[1][0]
#        ending_y = point_matrix[1][1]
#        # Draw rectangle for area of interest
#        cv2.rectangle(img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 3)
# 
        # Cropping image
    #    img_cropped = img[starting_y:ending_y, starting_x:ending_x]
    #    cv2.imshow("ROI", img_cropped)
 
    # Showing original image
    #cv2.imshow('image', img)
    #cv2.imshow("Original Image ", img)
    # Mouse click event on original image
#    cv2.setMouseCallback("image", mousePoints)
    # Printing updated point matrix
#    print(point_matrix)
    # Refreshing window all time
#    cv2.waitKey(1)