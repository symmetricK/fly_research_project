import cv2 # opencv
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
import json
import subprocess
import pdb
import glob



# create sorted images list
img_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames"
data_path=os.path.join(img_dir,'99*jpg')
files=glob.glob(data_path)
sorted_files=sorted(files)

# set seconds for text
sec=0

# create trap imgs with text 
for file in sorted_files:
	if sec<=500:
		font=cv2.FONT_HERSHEY_SIMPLEX
		trap_img=cv2.imread(file)
		text=str(sec)+'sec'
		if len(str(sec))==1:
			output='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/text_imgs/sec_00'+str(sec)+'.png'
		elif len(str(sec))==2:
			output='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/text_imgs/sec_0'+str(sec)+'.png'
		elif len(str(sec))==3:
			output='/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/text_imgs/sec_'+str(sec)+'.png'
		text_img=cv2.putText(trap_img,text,(1150,80),font,3,(255,255,255),5)
		sec=sec+2
		cv2.imwrite(output,text_img)
		print('done '+str(sec))

# MEMO peak 15 flies, trap 206sec,plot 133


'''
scale_percent=200
w=int(test_img.shape[1]*scale_percent/100)
h=int(test_img.shape[0]*scale_percent/100)
dim = (w,h)
res_img1=cv2.resize(test_img,dim,interpolation=cv2.INTER_AREA)
'''

#[nrows,ncols,colors]=np.shape(test_img)
#b_img=np.int8(np.zeros((nrows,ncols)))

# create sorted plots list
plot_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G"
plot_path=os.path.join(plot_dir,'*png')
plots=glob.glob(plot_path)
plots_1=[]
plots_2=[]
for i in plots:
	if len(i)==107:
		plots_1.append(i)
	elif len(i)==108:
		plots_2.append(i)
sorted_plots=sorted(plots_1)+sorted(plots_2)


text_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/text_imgs"
text_path=os.path.join(text_dir,'*png')
text_files=glob.glob(text_path)
sorted_texts=sorted(text_files)

'''
texts_1=[]
texts_2=[]
texts_3=[]

for i in text_files:
	if len(i)==127:
		texts_1.append(i)
	elif len(i)==128:
		texts_2.append(i)
	elif len(i)==129:
		texts_3.append(i)
sorted_texts=sorted(texts_1)+sorted(texts_2)+sorted(texts_3)
'''


sample_path=sorted_texts[0]
trap_img_sample=cv2.imread(sample_path)
shape=np.shape(trap_img_sample)
row,col=shape[1],shape[0]


ind=0


for plot in sorted_plots:
	plt_img=plot
	plot_img=cv2.imread(plot)
	res_plot_img=cv2.resize(plot_img, dsize=(row,col), interpolation=cv2.INTER_CUBIC)
	for text in sorted_texts:
		if sorted_plots.index(plot)==sorted_texts.index(text):
			text_img=cv2.imread(text)
			concat_img=cv2.hconcat([text_img,res_plot_img])
			if len(str(ind))==1:
				concat_output_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/concat_imgs/concat_"+'00'+str(ind)+'.png'
				cv2.imwrite(concat_output_dir,concat_img)
			elif len(str(ind))==2:
				concat_output_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/concat_imgs/concat_"+'0'+str(ind)+'.png'
				cv2.imwrite(concat_output_dir,concat_img)
			elif len(str(ind))==3:
				concat_output_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/concat_imgs/concat_"+str(ind)+'.png'
				cv2.imwrite(concat_output_dir,concat_img)
			ind+=1
			print('ind '+str(ind))





detect_in_img=cv2.imread("/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/final_in_on.jpg")
font=cv2.FONT_HERSHEY_SIMPLEX
text_in_img=cv2.putText(detect_in_img,'500sec',(1150,80),font,3,(255,255,255),5)
cv2.imwrite('/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/text_imgs/sec_500_in.png',text_in_img)

plot_in_img=cv2.imread("/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/trap_2021_10_30_G_RBRB.png")
res_plot_in_img=cv2.resize(plot_in_img, dsize=(row,col), interpolation=cv2.INTER_CUBIC)

concat_in_img=cv2.hconcat([text_in_img,res_plot_in_img])
concat_in_output_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/on_trap_detection_frames/concat_imgs/concat_999.png"
cv2.imwrite(concat_in_output_dir,concat_in_img)

'''
fig, axarr=plt.subplots(2,1)
axarr[0,0].imshow(test_img)
axarr[0,1].imshow(img2)
# create figure
fig=plt.figure()

#set row and colmn values
rows=1
columns=2


 Adds a subplot at the 1st position
fig.add_subplot(rows,columns,1)
plt.imshow(test_img)
plt.axis('off')

fig.add_subplot(rows,columns,2)
plt.imshow(img2)
plt.axis('off')

plt.savefig(output)
'''