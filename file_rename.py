import os
import glob
import pdb


date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")
y_n=input("Do you want to remove the even-numbered images?(y or n): ")

path='/home/flyranch/field_data_and_analysis_scripts/2021lab/'
src_path=path+'trapcam_timelapse/'+date+'/'

for it in os.scandir(src_path):
    if it.is_dir():
    	### rename image files
    	data_path=os.path.join(it,'*jpg')
    	filelist=glob.glob(data_path)
    	sorted_files=sorted(filelist)


    	count=1
    	for file in sorted_files:
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
    		dis=len(it.path)
    		time=file[dis+14:dis+20] #for 20220804 exp
    		ext=".jpg"
    		filename=pre+mid+time+ext
    		dst=it.path+"/"+filename
    		os.rename(file,dst)
    		count=count+1

    	### remove the even-numbered image files
    	rm_files=sorted_files[1::2]
    	if y_n=='y':
    		for f in sorted_files:
    			for rm_file in rm_files:
    				#pdb.set_trace()
    				if f==rm_file:
    					try:
	    					os.remove(f)
	    				except:
	    					pass


    	### rename subdirectory
    	src_dir=it.path+'/'
    	dst_dir=it.path[:-18]+'trap_'+it.path[-18:]+'/'
    	os.rename(src_dir,dst_dir)
