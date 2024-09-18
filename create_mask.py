import numpy as np
import cv2 
import pdb
import sys
import glob
import os


image_dir=input("Enter a trap name (without trap_) you'd like to create a mask (e.g. Pi1_20240708081731): ")
date=input("Enter what date did you do this experiment (e.g. 20220725): ")
print("Double click to make 4 points for mask on the image")
print("To store vertex data, press [a] on the image")
print("After storing 4 vertex data, press [l]. Then, see the terminal")
#path="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/"+date+"/trap_"+image_dir
#path='/media/flyranch/data21/field_release/trapcam_timelapse/'+date+"/trap_"+image_dir
path='/media/flyranch/14TB_Backup/field_release/trapcam_timelapse/'+date+"/trap_"+image_dir
data_path=os.path.join(path,'*g')
filelist=glob.glob(data_path)
sorted_files=sorted(filelist)

img=cv2.imread(sorted_files[int(len(sorted_files)/2)]) ### perhaps, it needs to change to run properly 

#img=cv2.imread(sorted_files[-1500])
#print(int(len(sorted_files)/2))

# Resize image
scale_percent=50 # 50 for 2304*1296, 25 for 4608*2592
width=int(img.shape[1]*scale_percent / 100)
height=int(img.shape[0]*scale_percent / 100)
dim=(width, height)
image=cv2.resize(img,dim)


global x_lst,y_lst
x_lst=[]
y_lst=[]

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY

    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(image,(x,y),10,(255,0,0))
        mouseX,mouseY = x,y


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)


while(1):
    cv2.imshow('image',image)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX)
        print(mouseY)
        if (len(x_lst)<4):
            x_lst.append(int(mouseX))
            y_lst.append(int(mouseY))
        elif (len(x_lst)>=4):
            print(x_lst)
            print(y_lst)
            print("You saved 4 points already")
            yes_no=input("Do you want to use these 4 points to make mask? (y or n): ")
            if yes_no=='y':
                x_MAX=int(max(x_lst)*(100/scale_percent))
                x_MIN=int(min(x_lst)*(100/scale_percent))
                y_MAX=int(max(y_lst)*(100/scale_percent))
                y_MIN=int(min(y_lst)*(100/scale_percent))

                [nrows,ncols,colors]=np.shape(img)
                mask=np.int8(np.zeros((nrows,ncols)))
                mask[int(y_MIN):int(y_MAX),int(x_MIN):int(x_MAX)]=1
                file=path+"/mask.jpg"
                cv2.imwrite(file,mask)
                print("mask.jpg created")

                #pdb.set_trace()
                img[0:y_MIN,:]=1
                img[y_MAX:img.shape[0],:]=1
                img[:,0:x_MIN]=1
                img[:,x_MAX:img.shape[1]]=1

                filename=path+"/mask_check.jpg"
                cv2.imwrite(filename,img)
                print("please, check mask_check.jpg in "+path+" directory")
                sys.exit()
            elif yes_no=='n':
                x_lst=[]
                y_lst=[]
                print("Try again")
            else:
                x_lst=[]
                y_lst=[]
                print("Try again")


    elif k == ord('l'):
        print(x_lst)
        print(y_lst)
        if len(x_lst)==4:
            y_n=input("Do you want to use these 4 points to make mask? (y or n): ")
            if y_n=='y':
                x_MAX=int(max(x_lst)*(100/scale_percent))
                x_MIN=int(min(x_lst)*(100/scale_percent))
                y_MAX=int(max(y_lst)*(100/scale_percent))
                y_MIN=int(min(y_lst)*(100/scale_percent))

                [nrows,ncols,colors]=np.shape(img)
                mask=np.int8(np.zeros((nrows,ncols)))
                mask[int(y_MIN):int(y_MAX),int(x_MIN):int(x_MAX)]=1
                file=path+"/mask.jpg"
                cv2.imwrite(file,mask)
                print("mask.jpg created")

                #pdb.set_trace()
                img[0:y_MIN,:]=1
                img[y_MAX:img.shape[0],:]=1
                img[:,0:x_MIN]=1
                img[:,x_MAX:img.shape[1]]=1

                filename=path+"/mask_check.jpg"
                cv2.imwrite(filename,img)
                print("please, check mask_check.jpg in "+path+" directory")
                sys.exit()
            elif y_n=='n':
                x_lst=[]
                y_lst=[]
                print("Try again")
            else:
                x_lst=[]
                y_lst=[]
                print("Try again")


cv2.destroyAllWindows()