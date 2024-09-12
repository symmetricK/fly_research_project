import os
import os.path
import glob
import shutil
import pdb

date=input("Enter what date did you do this experiment (e.g. 20220317 (yyyymmdd)): ")
path='/media/flyranch/data21/field_release/Field_Trap_Exps/'
outpath='/home/flyranch/field_data_and_analysis_scripts/2021lab/trapcam_timelapse/'

src_path=path+date[:4]+"-"+date[4:6]+"-"+date[6:]

dst_path=outpath+date+'/'

shutil.copytree(src_path,dst_path)

### if anemometer data file exists, copy and rename
txt_path=src_path+'/*.txt'
txt_dst_path=path+'wind_data_files/'
txt_file=glob.glob(txt_path)
new_name=txt_dst_path+'anemometer_'+date[:4]+'_'+date[4:6]+'_'+date[6:]+'.txt'

if len(txt_file)==1:
	shutil.copy(txt_file[0],txt_dst_path)
	wind_file=glob.glob(txt_dst_path+'/*'+date[4:]+'*.txt')
	os.rename(wind_file[0],new_name)
