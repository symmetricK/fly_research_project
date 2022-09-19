import pandas as pd
from math import radians
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time
import datetime
#from datetime import datetime
import sys
import json
import glob
import os
import json
import re


def get_vec_list(alpha,**kwargs):
    nvls=1e4
    vals_list=[]
    for crind, cr_alpha in enumerate(alpha):
        num_vls_to_add=np.round(kwargs['weights'][crind]*nvls)
            
        vals_list=np.append(vals_list,cr_alpha*np.ones(int(num_vls_to_add)))
    return vals_list


def circmean(alpha,axis=None, **kwargs):
    
    if 'weights' in kwargs:
        
        vals_list=get_vec_list(alpha,**kwargs)
        
        N=len(vals_list)
       
        mean_angle = np.arctan2(np.nanmean(np.sin(vals_list),axis),np.nanmean(np.cos(vals_list),axis))
    else:
        mean_angle = np.arctan2(np.nanmean(np.sin(alpha),axis),np.nanmean(np.cos(alpha),axis))
    
    return mean_angle


def circvar(alpha,axis=None,**kwargs):
    if np.ma.isMaskedArray(alpha) and alpha.mask.shape!=():
        N = np.sum(~alpha.mask,axis)
    else:
        if axis is None:
            N = alpha.size
        else:
            N = alpha.shape[axis]
    
    #this is accomplished in an inelegant manner,
    #where I asemble 10,000 values proportioned according to the weights, and then compute.
    if 'weights' in kwargs:
        

        vals_list=get_vec_list(alpha,**kwargs)
        
        N=len(vals_list)
        R = np.sqrt(np.sum(np.sin(vals_list),axis)**2 + np.sum(np.cos(vals_list),axis)**2)/N
    else:
        R = np.sqrt(np.sum(np.sin(alpha),axis)**2 + np.sum(np.cos(alpha),axis)**2)/N

    ### R is the length of the average of random vectors on the unit circle
    ###The circular variance, V, is a measure of variation in the data. Note that V=1-R 
    V = 1-R
    return V


def wind_direction_converter(w_dir,axis=None):
    ### convert from wind direction to math direction in rad
    math_d=270-w_dir # need to convert from weather direction to math angle
    if math_d<0:
        math_d=math_d+360
    rad=np.deg2rad(math_d)
    return rad

def calc_mean_wind_speed(w_spd,u_component,v_component):
    ### calculate 3 average wind speeds in different ways
    
    ### Scalar Average (the mean of the wind magnitudes (speed), not taking into account the wind direction) 

    ### The scalar mean wind speed over a period of interest can be obtained in two ways:
        ### 1. calculating wind speed from the components u and v for each time step and then averaging over the period;
        ### 2. averaging the wind_speed from the product over the period.

    N=len(w_spd)
    ws_a=np.sum(w_spd)/N
    
    ws_b_lst=[]
    for a, b in zip(u_component,v_component):
        ws_B=np.sqrt(a**2+b**2)
        ws_b_lst.append(ws_B)
    ws_b=sum(ws_b_lst)/N
       
    ### Vector Average (takes into account the wind direction)
    ### The vector mean wind speed is obtained by first averaging u and v over the period of interest
    ### and then calculating the wind_speed from the averaged u and v.
    ### when direction matters
    
    ws_u_list=[]
    ws_v_list=[]
    for i in u_component:
        ws_u_list.append(i)
    for j in v_component:
        ws_v_list.append(j)    
    ws_c_u=sum(ws_u_list)/N
    ws_c_v=sum(ws_v_list)/N    
    ws_c=np.sqrt(ws_c_u**2+ws_c_v**2)
    return ws_a,ws_b,ws_c

def parm_calculator(df):
    ### calculate parameters for wind circular plot
    v=1-circvar(df.direction)
    a=circmean(df.direction)
    s=np.sum(df.wind_speed)/len(df)
    x,y,z=calc_mean_wind_speed(df.wind_speed,df.U,df.V)
    
    ### for release experiments, only need a,z (angle and vector ave wind spd)
    return  a,z

def calc_sec_since_release(standard,time_stamp):
    zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])+1
    sec=int(time_stamp[0:2])*3600+int(time_stamp[3:5])*60+int(time_stamp[6:8])
    sec_since_release=sec-zero
    return sec_since_release

def make_accumulation_list(list):
    acc_list=[]
    for i in range(len(list)):
        ele=np.sum(list[:i+1])
        acc_list.append(ele)
    return acc_list



date=input("what date did you release flies (e.g. 20220804): ")
release=input("what time did you release flies (e.g. 105542): ")

path='/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/'

list_of_files= sorted(glob.glob(path+date+'/*/master_*.json'))

released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]
master_fly_pop_dict={}

for file in list_of_files:
    f=open(file)
    data=json.load(f)
    #create lists
    on_trap_list=[]
    in_trap_list=[]
    sec_since_release_list=[]
    actual_timestamp_list=[]

    string=file
    pattern='master'
    match=(re.search(pattern, string))

    trap_name=string[match.end()+6:-5] ###remove 'master_trap_' and '.json'
    t_name=string[match.end()+6:match.end()+9] ###Pi_X

    for i in data['trap_'+trap_name]:
        for k in data['trap_'+trap_name][i]:
            if i=="flies on trap over time:":
                on_trap_list.append(k)
            elif i=="flies in trap over time:":
                in_trap_list.append(k)
            elif i=="actual timestamp:":
                if len(str(int(k)))==5:
                    str_time='0'+str(int(k))[0:1]+':'+str(int(k))[1:3]+':'+str(int(k))[3:5]
                    actual_timestamp_list.append(str_time)
                elif len(str(int(k)))==6:
                    str_time=str(int(k))[0:2]+':'+str(int(k))[2:4]+':'+str(int(k))[4:6]
                    actual_timestamp_list.append(str_time)
    f.close()
        
    on_trap_acc_list=make_accumulation_list(on_trap_list)
    
    for i in actual_timestamp_list:
        s=calc_sec_since_release(released_time,i)
        sec_since_release_list.append(s)
        
    new_sec_since_release_list=[]        
    fly_pop_list=[]
    
    for i in sec_since_release_list:
        if (i%60==0) or (i%60==1):
            if 0<=i<=901: ###0-15mins     
                new_sec_since_release_list.append(i)
                fly_pop_list.append(int(on_trap_acc_list[sec_since_release_list.index(i)]))
    
    fly_pop_dict={t_name:fly_pop_list}            
    master_fly_pop_dict.update(fly_pop_dict)

#print(master_fly_pop_dict)
#print((list(master_fly_pop_dict.values())[0][0]))

P=list(master_fly_pop_dict.values())

data_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/anemometer_"
directory=data_path+date[:4]+"_"+date[4:6]+"_"+date[6:]+".txt"

df=pd.read_csv(directory,delimiter=' ',header=None)
df.columns=("time","direction","wind_speed")

time_list=[]
angle_list=[]
spd_list=[]
u_lst=[]
v_lst=[]

for i in df.iloc[:,0]:
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
    int_time=int(str_time[:2])*60+int(str_time[2:4])
    int_release=int(release[:2])*60+int(release[2:4])
    time_list.append(int_time-int_release)

df.iloc[:,0]=time_list


for i in df.iloc[:,1]:
    angle_rad=wind_direction_converter(i)
    angle_list.append(angle_rad)
df.iloc[:,1]=angle_list

for i in df.iloc[:,2]:
    spd=i*0.44704 # convert mph to m/s
    spd_list.append(spd)     
df.iloc[:,2]=spd_list

for a, b in zip(spd_list,angle_list):
    V=a*np.sin(b)
    v_lst.append(V)
    U=a*np.cos(b)
    u_lst.append(U)  
    
df["U"]=u_lst
df["V"]=v_lst

new_df=df[0<=df.time] # time converted in "minutes since release"
trimmed_df=new_df[new_df.time<=15]
set_df1=trimmed_df[trimmed_df.time<4]
set_df2=trimmed_df[(4<=trimmed_df.time)&(trimmed_df.time<8)]
set_df3=trimmed_df[(8<=trimmed_df.time)&(trimmed_df.time<12)]
set_df4=trimmed_df[trimmed_df.time>=12]

a1,z1=parm_calculator(set_df1)
a2,z2=parm_calculator(set_df2)
a3,z3=parm_calculator(set_df3)
a4,z4=parm_calculator(set_df4)

m_angle_lst=[a1,a2,a3,a4]
ws_lst=[z1,z2,z3,z4]

#set_lst=set(trimmed_df.time)
#for i in set_lst:
#    set_df=trimmed_df[trimmed_df.time==i]
#    v=1-circvar(set_df.direction)
#    v_str_lst.append(v)
#    a=circmean(set_df.direction)
#    m_angle_lst.append(a)
#    s=np.sum(set_df.wind_speed)/len(set_df)
#    m_spd_lst.append(s)
#    x,y,z=calc_mean_wind_speed(set_df.wind_speed,set_df.U,set_df.V)
#    ws_lst.append(z)
#print(len(v_str_lst))
#print(m_angle_lst)
#print(m_spd_lst)
#print(ws_lst)


fig=plt.figure(figsize=(35,30))
fig.suptitle(date+" Average Vector Wind Speed and Accumulated Number of Flies on Trap at Specific Times",fontsize=40)
a=2 #number of rows 
b=2 #number of columns
c=1 #plot counter
    
while(c<5):
#    v=v_str_lst[c-1]
    m=m_angle_lst[c-1]
    w=ws_lst[c-1]
    r=[0,w]   # r would be mean wind speed
    theta=[m,m]   ### theta would be mean angle
    ax=plt.subplot(a,b,c, polar=True)
    ax.set_theta_zero_location('E')
    ax.set_theta_direction('counterclockwise')
    ax.set_yticks([.5,1])
    ax.set_yticklabels(['0.5 m/s','1 m/s'],fontsize=15)
    ax.set_ylim([0,1])
    ax.plot(theta,r,lw=4)
    ax.text(m,w+0.1,str(round((w),3))+"m/s",fontsize=20)
    ax.set_xticks([0,np.pi/8,np.pi*3/8,np.pi/2,np.pi*5/8,np.pi*7/8,np.pi,
                   np.pi*9/8,np.pi*11/8,np.pi*3/2,np.pi*13/8,np.pi*15/8])
    ax.set_rlabel_position(45) ### change ytick label position (degree)
    
    if c==1:
        ax.set_title("0-3mins",fontsize=30)
        ax.set_xticklabels(['E','Pi7:'+str(P[6][0:4]),'Pi6:'+str(P[5][0:4]),'N',
                            'Pi5:'+str(P[4][0:4]),'Pi4:'+str(P[3][0:4]),
                        'W','Pi3:'+str(P[2][0:4]),'Pi2:'+str(P[1][0:4]),'S',
                            'Pi1:'+str(P[0][0:4]),'Pi8:'+str(P[7][0:4])],fontsize=20)
    elif c==2:
        ax.set_title("4-7mins",fontsize=30)
        ax.set_xticklabels(['E','Pi7:'+str(P[6][4:8]),'Pi6:'+str(P[5][4:8]),'N',
                            'Pi5:'+str(P[4][4:8]),'Pi4:'+str(P[3][4:8]),
                        'W','Pi3:'+str(P[2][4:8]),'Pi2:'+str(P[1][4:8]),'S',
                            'Pi1:'+str(P[0][4:8]),'Pi8:'+str(P[7][4:8])],fontsize=20)
    elif c==3:
        ax.set_title("8-11mins",fontsize=30)
        ax.set_xticklabels(['E','Pi7:'+str(P[6][8:12]),'Pi6:'+str(P[5][8:12]),'N',
                            'Pi5:'+str(P[4][8:12]),'Pi4:'+str(P[3][8:12]),
                        'W','Pi3:'+str(P[2][8:12]),'Pi2:'+str(P[1][8:12]),'S',
                            'Pi1:'+str(P[0][8:12]),'Pi8:'+str(P[7][8:12])],fontsize=20)
    elif c==4:
        ax.set_title("12-15mins",fontsize=30)
        ax.set_xticklabels(['E','Pi7:'+str(P[6][12:]),'Pi6:'+str(P[5][12:]),'N',
                            'Pi5:'+str(P[4][12:]),'Pi4:'+str(P[3][12:]),
                        'W','Pi3:'+str(P[2][12:]),'Pi2:'+str(P[1][12:]),'S',
                            'Pi1:'+str(P[0][12:]),'Pi8:'+str(P[7][12:])],fontsize=20)
    c+=1

 

save_path='/home/flyranch/field_data_and_analysis_scripts/2021lab/analyzed_plot_figures/'
ex_path=save_path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.mkdir(ex_path)

plt.savefig(ex_path+'/'+date+'_circ_wind_and_acc_ontrap_plot.jpg')