## import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import pandas as pd
import time
import datetime
import os


##### wind speed-time plot with wind direction #####


date=input("what date did you release flies (e.g. 20220804): ")
wind_data=date[:4]+"_"+date[4:6]+"_"+date[6:]
release=input("what time did you release flies (e.g. 142040): ")
data_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/anemometer_"

directory=data_path+wind_data+".txt"
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
#    str_time=str_h+str_m+str_s # include seconds
    str_time=str_h+str_m
    time_list.append(str_time)
    
wind_df.iloc[:,0]=time_list

rad_d_list=[]
mean_angle_list=[]

for i in range(len(wind_df)): 
    math_d=270-wind_df['direction'][i] # need to convert from weather direction to math angle
    if math_d<0:
        math_d=math_d+360
    rad=np.deg2rad(math_d) # convert to degree to radian
    if i==0:
        rad_d_list.append(rad)
    if (i!=0) and (wind_df['time'][i]==wind_df['time'][i-1]):
        if i==(len(wind_df)-1):
            rad_d_list.append(rad)
            mean_angle=np.arctan2(np.nanmean(np.sin(rad_d_list)),np.nanmean(np.cos(rad_d_list)))    
            mean_angle_list.append(mean_angle)
        else:
            rad_d_list.append(rad)
    if (i!=0) and (wind_df['time'][i]!=wind_df['time'][i-1]):
        if i==(len(wind_df)-1):
            rad_d_list.append(rad)
            mean_angle=np.arctan2(np.nanmean(np.sin(rad_d_list)),np.nanmean(np.cos(rad_d_list)))    
            mean_angle_list.append(mean_angle)
        else:       
            mean_angle=np.arctan2(np.nanmean(np.sin(rad_d_list)),np.nanmean(np.cos(rad_d_list)))    
            mean_angle_list.append(mean_angle)
            rad_d_list=[]
            rad_d_list.append(rad)

new_wind_df=wind_df.groupby(['time'], as_index=False).mean()
new_wind_df['direction']=mean_angle_list

new_t_list=new_wind_df['time']
new_s_list=new_wind_df['wind_speed']*0.44704 # convert mph to m/s
new_d_list=new_wind_df['direction'] 
new_n_list=list(np.arange(1,len(new_t_list)+1))

fig=plt.figure(figsize=(20,10))
ax=plt.axes()

plt.plot(new_n_list, new_s_list, '-',markersize=6,color="r")
plt.title(date+' Time-Speed with Wind Direction')
plt.xlabel('Time')
plt.ylabel('Wind Speed (m/s)')
ax.set_xticks(new_n_list)
ax.set_xticklabels(new_t_list,rotation=45)
x_min=np.min(new_n_list)
x_max=np.max(new_n_list)
y_min=np.min(new_s_list)
y_max=np.max(new_s_list)

ratio=(x_max-x_min)/(y_max-y_min) # to adjust arrow length

for i in range(len(new_n_list)):
    dx=(np.cos(new_d_list[i]))
    dy=(np.sin(new_d_list[i]))
    ax.annotate("",xy=(new_n_list[i],new_s_list[i]),
               xytext=(new_n_list[i]+dx,
                       new_s_list[i]+3*(dy/ratio)),arrowprops=dict(arrowstyle='-'))
    if new_t_list[i]==release[:4]:
        ax.axvline(x=i+1,ymax=y_max,ls='--',color='b')


save_path='/home/flyranch/field_data_and_analysis_scripts/2021lab/analyzed_plot_figures/'
ex_path=save_path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.mkdir(ex_path)

plt.savefig(ex_path+'/'+date+'_wind_time_plot.svg')

