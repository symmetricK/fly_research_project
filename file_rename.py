import numpy as np
import os
import glob
import pdb

directry=input("Enter a directory name (without trap_) which has files you'd like to rename: ")
#directry="2022_03_17_WT"

o_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_"+directry
data_path=os.path.join(o_dir,'*jpg')
filelist=glob.glob(data_path)
sorted_files=sorted(filelist)
rm_files=sorted_files[1::2]

date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")
#date="20220317"

### remove the same hh/mm/ss files (to make 1 frame/second)
for f in sorted_files:
	for file in rm_files:
		if f==file:
			os.remove(file)


data_path2=os.path.join(o_dir,'*jpg')
filelist2=glob.glob(data_path2)
sorted_files2=sorted(filelist2)

### rename files
count=1
for file2 in sorted_files2:
	if count<10:
		c="000"+str(count)
	elif 10<=count<100:
		c="00"+str(count)
	elif 100<=count<1000:
		c="0"+str(count)
	else:
		c=str(count)

	pre="tl_0000_"+c+"_"
	mid=date+"_"
	dis=len(o_dir)
	time=file2[dis+1:dis+3]+file2[dis+4:dis+6]+file2[dis+7:dis+9]
	ext=".jpg"

	filename=pre+mid+time+ext
	dst=o_dir+"/"+filename
	os.rename(file2,dst)
	count=count+1




