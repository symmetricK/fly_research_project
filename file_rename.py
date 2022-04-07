import numpy as np
import os
import glob
import pdb
import re

before_dir=input("Enter a directory which has files you'd like to rename: ")
b_dir="/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/trap_"+before_dir
data_path=os.path.join(b_dir,'*g')
filelist=glob.glob(data_path)

count=1

date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")



for file in filelist:
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

	dis=len(b_dir)
	time=file[dis+1:dis+3]+file[dis+4:dis+6]+file[dis+7:dis+9]
	ext=".jpg"
	filename=pre+mid+time+ext
	pdb.set_trace()



###to discard before time= pattern match w/ b_dir 

### decimal = mjust discard

