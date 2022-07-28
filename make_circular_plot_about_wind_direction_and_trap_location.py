## import pandas as pd
from math import radians
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time
import datetime
import sys
import json
import pandas as pd

wind_data=input("Enter wind data text file you would like to make a circular plot (e.g. 2021_10_19): ")

directory="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/wind_"+wind_data+".txt"
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

a_wind_df=wind_df.groupby(['time'], as_index=False).mean()
a_wind_df['direction']=mean_angle_list
a_wind_df['wind_speed']=a_wind_df['wind_speed']*0.44704 # convert mph to m/s



#I=15.0 # degree for trap I
#J=195.0 # degree for trap J

#theta1=np.deg2rad([I,I]) # trap I
#theta2=np.deg2rad([J,J]) # trap J
r=[0,1.0]

min_len=5 # initial 5min

fig1=plt.figure(figsize=(30,20))

a=1 #number of rows
b=5 #number of columns
c=1 #plot counter

release_time=input("what time did you release flies (e.g. 1420): ")

dir_list=[]
spd_list=[]

for i in range(len(a_wind_df)):
    if 1421<=int(a_wind_df['time'][i])<=1425:
        dir_list.append(a_wind_df['direction'][i])
        spd_list.append(a_wind_df['wind_speed'][i])
        
rad_dir_list=np.deg2rad(90-np.rad2deg(dir_list))

for i in np.arange(min_len):
    ax1=plt.axes()
    ax1=plt.subplot(a,b,c, polar=True)
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction('clockwise')
    ax1.set_yticks([])
    ax1.plot(theta1,r,'r')
    ax1.plot(theta2,r,'b')
    ax1.text(np.radians(I),ax1.get_rmax()+0.15,'trap I (15°)',
            ha='center',va='center')
    ax1.text(np.radians(J),ax1.get_rmax()+0.15,'trap J (195°)',
            ha='center',va='center')
    ax1.text(np.radians(0),ax1.get_rmax()+0.4,str(release_time+c)[:2]+':'+str(release_time+c)[2:4]+
             '\n'+str(round(spd_list[i],3))+ 'm/s',
            ha='center',va='center')
    wind_d_theta=[rad_dir_list[i],rad_dir_list[i]]
    ax1.plot(wind_d_theta,[0,spd_list[i]],marker='X',ls='--',color='k')
    c=c+1

path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_plot_figures/"

plt.savefig(path+wind_data+'_wind_d_circular_plot.svg')
