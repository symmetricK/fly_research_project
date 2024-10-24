a
import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import pandas as pd
import time
import datetime
import os
import matplotlib
##### box and whisker plot of wind speed for 3 minutes after fly release #####


date_list=["20230621","20230630","20230725","20230731","20230808","20231003",
           "20231008","20231012","20240630","20240708","20240716","20240724",
           "20240807","20240819","20240826","20240905","20240910","20240923","20241006"]
#"20220804","20220914","20220923"
#"20190706","20190611","20190508","20190419"
release_list=["123200","094055","113037","105622","094526","154610",
              "122251","135550","112239","090049","094420","082053",
              "074202","081047","082421","084649","082316","082010","101551"]
#"105542","113540","114246"
#"081100","074800","100400","115600"
#date=input("what date did you,release flies (e.g. 20220804): ")
#date="20230731"
#wind_data=date[:4]+"_"+date[4:6]+"_"+date[6:]
#release=input("what time did you release flies (e.g. 142040): ")
#release="105622"
#data_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/anemometer_"

data_list=[]

for date in date_list:
    wind_data=date[:4]+"_"+date[4:6]+"_"+date[6:]
    release=release_list[date_list.index(date)]
    #print(release)
    #data_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/anemometer_"
    data_path="/media/flyranch/14TB_Backup/field_release/wind_data_files/"
    directory=data_path+"anemometer_"+wind_data+".txt"
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
        str_time=str_h+str_m+str_s # include seconds
        #str_time=str_h+str_m
        int_time=int(str_h)*3600+int(str_m)*60+int(str_s)
        time_list.append(int_time)

    ### adjust
    wind_df.iloc[:,0]=time_list
    ### focus on 5minutes after release
    release_in_sec=int(release[:2])*3600+int(release[2:4])*60+int(release[4:])
    release_in_sec_plus_3min=release_in_sec+180
    #this_time=int(wind_df['time'][:2])*3600+int(wind_df['time'][2:4])*60+int(wind_df['time'][4:])
    new_wind_df=wind_df.loc[(release_in_sec<=wind_df['time'])&(wind_df['time']<=release_in_sec_plus_3min)]
    #new_wind_df=wind_df.loc[(release<=wind_df['time'])&(wind_df['time']<=str(int(release)+5))]   

    td_list=[]
    #print(new_wind_df.iloc[:,0])
    #for i in new_wind_df.iloc[:,0]:
    #    if int(i)<36000:
    #        td=str(timedelta(seconds=i))[:1]+str(timedelta(seconds=i))[2:4]+str(timedelta(seconds=i))[5:7]
    #    else:
    #        td=str(timedelta(seconds=i))[:2]+str(timedelta(seconds=i))[3:5]+str(timedelta(seconds=i))[6:8]
    #    td_list.append(td)
        
    #new_wind_df.iloc[:,0]=td_list
    spd_list=new_wind_df['wind_speed']*.44704 # convert mph to m/s

    matplotlib.rcParams['pdf.fonttype'] = 42
    green_diamond = dict(markerfacecolor='g', marker='D')
    data=spd_list
    data_list.append(data)

fig,ax=plt.subplots(figsize=(12,8))
#ax.set_title("box and whisker plot of wind speed for 3 minutes after fly release \n the last 4 from Kate Leitch's data")
ax.set_title("box and whisker plot of wind speed for 3 minutes after fly release")
ax.boxplot(data_list, flierprops=green_diamond)
ax.set_xticklabels(date_list,rotation=45)
ax.set_ylabel("wind speed (m/s)")

out_path=data_path+"wind_data_plots/boxplot_for_wind_data.pdf"

#plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/wind_data_plots/boxplot_for_wind_data.pdf')
