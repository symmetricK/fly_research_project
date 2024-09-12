import os
import glob
import pdb


date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")
#y_n=input("Do you want to remove the even-numbered images?(y or n): ")

#d=date[:4]+'-'+date[4:6]+'-'+date[6:8]

#path='/home/flyranch/field_data_and_analysis_scripts/2021lab/'
#path='/media/flyranch/data21/field_release/Field_Trap_Exps/'
#path='/media/flyranch/data21/field_release/'
path='/media/flyranch/14TB_Backup/field_release/'
src_path=path+'trapcam_timelapse/'+date+'/'

for it in os.scandir(src_path):
    if it.is_dir():
    	#pdb.set_trace()
    	### rename image files
    	data_path=os.path.join(it,'*jpg')
    	filelist=glob.glob(data_path)
    	sorted_files=sorted(filelist)


    	#pdb.set_trace()
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
    		time=file[-16:-10]
    		ext=".jpg"
    		filename=pre+mid+time+ext
    		dst=it.path+"/"+filename
    		if 'mask' not in file:
    			os.rename(file,dst)
    			count=count+1

    	### remove the even-numbered image files
    	#rm_files=sorted_files[1::2]
    	#if y_n=='y':
    	#	for f in sorted_files:
    	#		for rm_file in rm_files:
    	#			#pdb.set_trace()
    	#			if f==rm_file:
    	#				try:
	    #					os.remove(f)
	    #				except:
	    #					pass

'''
    	### rename subdirectory
    	src_dir=it.path+'/'
    	Pi_nums='Pi10','Pi11','Pi12','Pi13','Pi14','Pi15','Pi16'
    	if any(i in it.path for i in Pi_nums):
    		dst_dir=it.path[:-19]+'trap_'+it.path[-19:]+'/'
    	else:
    		dst_dir=it.path[:-18]+'trap_'+it.path[-18:]+'/'
    	os.rename(src_dir,dst_dir)
'''