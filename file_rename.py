import numpy as np
import os
import glob
import pdb

before_dir=input("Enter a directory name (without trap_) which has files you'd like to rename: ")
b_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_"+before_dir
data_path=os.path.join(b_dir,'*g')
filelist=glob.glob(data_path)
sorted_files=sorted(filelist)

date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")
files=glob.glob(data_path)
sorted_files=sorted(files)

count=1


for file in sorted_files:
	mid=date+"_"
	dis=len(b_dir)
	time=file[dis+1:dis+3]+file[dis+4:dis+6]+file[dis+7:dis+9]
	t=time[:2]+"-"+time[2:4]+"-"+time[4:6]
	ext=".jpg"
	pdb.set_trace()
	test=glob.glob(b_dir+"/"+t+"*"+ext)

	if os.path.exists(b_dir+"/"+time+"*"+ext):
		if os.path.exists(b_dir+"/"+t+"*"+ext):
			print(b_dir+"/"+t+"*"+ext)
			os.remove(b_dir+"/"+t+"*"+ext)

(b_dir+"/"+t+"*"+ext)


	else:
		if count<10:
			c="000"+str(count)
		elif 10<=count<100:
			c="00"+str(count)
		elif 100<=count<1000:
			c="0"+str(count)
		else:
			c=str(count)
		pre="tl_0000_"+c+"_"

		filename=pre+mid+time+ext
		os.rename(file,b_dir+"/"+filename)
		count=count+1

#	pdb.set_trace()



###to discard before time= pattern match w/ b_dir 

### decimal = mjust discard

