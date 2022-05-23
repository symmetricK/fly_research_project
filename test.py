import cv2
import pdb
import numpy as np
from sys import exit
import math

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks (location)
	if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
		print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img, str(x) + ',' +
					str(y), (x,y), font,
					1, (255, 0, 0), 2)
		cv2.imshow('image', img)

    # checking for right mouse clicks (color)
	if event==cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
		print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
		font = cv2.FONT_HERSHEY_SIMPLEX
		b = img[y, x, 0]
		g = img[y, x, 1]
		r = img[y, x, 2]
		cv2.putText(img, str(b) + ',' +
					str(g) + ',' + str(r),
					(x,y), font, 1,
					(255, 255, 0), 2)
		cv2.imshow('image', img)


# functiont to calculate distance between two points
def calculateDistance(x1,y1,x2,y2):
  dist=math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
  return dist

# driver function
if __name__=="__main__":
	# reading the image
	dst=input("which image?: ")
	#dst='/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_2021_10_30_J/tl_0000_0001_20211030_134330.jpg'

	img=cv2.imread(dst)
	cv2.namedWindow("image",cv2.WINDOW_NORMAL)
	# displaying the image
	cv2.imshow('image', img)

#	if cv2.getWindowProperty('image', 0)<0:
#		sys.exit()


	# setting mouse handler for the image
	# and calling the click_event() function
	cv2.setMouseCallback('image', click_event)

	print("Click on two center of funnels")
	print("Note how many center of funnels there are between two points excluding the two points")
	print("To quit, press 'q', or press X button on the image window")

	## wait for a key to be pressed to exit
#	cv2.waitKey(0)
	# close the window
#	cv2.destroyAllWindows()



	while True:
		if cv2.waitKey(1)==ord('q'):
			break
		if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE)<1:
			break

	# close the window
	cv2.destroyAllWindows()



	x1=input('Type the x coordinate of the first point (x1): ')
	y1=input('Type the y coordinate of the first point (y1): ')
	x2=input('Type the x coordinate of the second point (x2): ')
	y2=input('Type the y coordinate of the second point (y2): ')
	n=input('Type how many center of funnels there are between two points excluding the two points: ')

	length=calculateDistance(int(x1),int(y1),int(x2),int(y2))
	ave_len=length/(int(n)+1)

	print(ave_len)
#	while cv2.getWindowProperty('image',0)>=0:

 

	#cv2.destroyAllWindows()

	#if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
#		print("ALL WINDOWS ARE CLOSED")
#	cv2.waitKey(1)

