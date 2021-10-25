import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import os
import glob
import sys
import pandas as pd
import time
import datetime

wind_data=input("Enter wind data text file you would like to convert to a wind data json file (e.g. 2021_10_19): ")

directory="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/"+wind_data+".txt"
wind_df=pd.read_csv(directory,delimiter=' ',header=None)
wind_df.columns=("time","direction","wind_speed")

time_list=[]

for i in wind_df.iloc[:,0]:
    time=datetime.datetime.fromtimestamp(i)
    str_h=str(time.hour)
    str_m=str(time.minute)
    str_s=str(time.second)
    if len(str_h)==1:
        str_h='0'+str_h
    if len(str_m)==1:
        str_m='0'+str_m
    if len(str_s)==1:
        str_s='0'+str_s
    str_time=str_h+str_m+str_s
    time_list.append(str_time)
    
wind_df.iloc[:,0]=time_list

#new_wind_df=wind_df.groupby(['time'], as_index=False).mean()
new_wind_df=wind_df.groupby(['time']).mean()
test_json=new_wind_df.to_json


pdb.set_trace()

new_t_list=new_wind_df['time']
new_w_list=new_wind_df['wind_speed']
new_d_list=new_wind_df['direction']

#pdb.set_trace()

wind_dict={"t":new_t_list,"d":new_d_list,"w":new_w_list}

json_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/"+wind_data+".json"

#parsed = json.loads(result)

#json.dumps(parsed, indent=4)  

with open(json_path,'w') as json_file:
	json.dump(test_json,json_file,indent=1)

#if not os.path.exists(json_path):
#    with open(json_path,'w') as json_file:
#        json.dump(wind_dict,json_file,indent=1)
#else:
#	y_n=input("master json file has alredy exists. Do you want to overwrite it? (y or n): ")
#	if y_n=="y":
#		print('master json file was overwritten')
#		with open(json_path,'w') as json_file:
#			json.dump(wind_dict,json_file,indent=1)
#	if y_n=="n":
#		sys.exit()