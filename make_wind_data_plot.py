import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import pandas as pd
import time
import datetime
import os
import matplotlib


##### wind speed-time plot with wind direction #####


date=input("what date did you release flies (e.g. 20220804): ")
#date='20241006'
wind_data=date[:4]+"_"+date[4:6]+"_"+date[6:]
release=input("what time did you release flies (e.g. 142040): ")
#release='101551'
#data_path="/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files/anemometer_"
#data_path='/media/flyranch/data21/field_release/wind_data_files/anemometer_'
data_path="/media/flyranch/14TB_Backup/field_release/wind_data_files/"
wind_txt=data_path+"anemometer_"+wind_data+".txt"
#out_path='/media/flyranch/data21/field_release/wind_data_files/wind_data_plots/'
out_path=data_path+"wind_data_plots/"

wind_df=pd.read_csv(wind_txt,delimiter=' ',header=None)
wind_df.columns=("time","wind_direction","wind_speed")

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
    math_d=270-wind_df['wind_direction'][i] # need to convert from weather direction to math angle
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

new_wind_df.insert(2,"math_direction",mean_angle_list, True)
#new_wind_df['direction']=mean_angle_list

num=new_wind_df[new_wind_df['time']==release[:4]].index[0]
#print(num)
fil_wind_df=new_wind_df.iloc[num-5:num+35,:]
#print(fil_wind_df)
filtered_wind_df=fil_wind_df.reset_index()

#print(filtered_wind_df)

'''
new_t_list=new_wind_df['time']
new_s_list=new_wind_df['wind_speed']*0.44704 # convert mph to m/s
#new_d_list=new_wind_df['direction']
new_d_list=new_wind_df['math_direction']
new_n_list=list(np.arange(1,len(new_t_list)+1))
'''

new_t_list=filtered_wind_df['time']
new_s_list=filtered_wind_df['wind_speed']*0.44704 # convert mph to m/s
#new_d_list=new_wind_df['direction']
new_d_list=filtered_wind_df['math_direction']
new_n_list=list(np.arange(1,len(new_t_list)+1))

matplotlib.rcParams['pdf.fonttype'] = 42

fig=plt.figure(figsize=(20,10))
ax=plt.axes()

plt.plot(np.array(new_n_list),np.array(new_s_list), '-',markersize=6,color="r")
plt.title(date+' Time-Speed with Wind Direction')
plt.xlabel('Time')
plt.ylabel('Wind Speed (m/s)')
ax.set_xticks(new_n_list)
ax.set_xticklabels(new_t_list,rotation=45)
ax.set_ylim(0,3)
x_min=np.min(new_n_list)
x_max=np.max(new_n_list)
y_min=np.min(new_s_list)
y_max=np.max(new_s_list)

ratio=(x_max-x_min)/(y_max-y_min) # to adjust arrow length


#print(range(len(new_n_list)))
#print(new_n_list)
#print(new_d_list)

for i in range(len(new_n_list)):
    dx=(np.cos(new_d_list[i]))
    dy=(np.sin(new_d_list[i]))
    ax.annotate("",xy=(new_n_list[i],new_s_list[i]),
               xytext=(new_n_list[i]+dx,
                       new_s_list[i]+3*(dy/ratio)),arrowprops=dict(arrowstyle='-'))
    if new_t_list[i]==release[:4]:
        ax.axvline(x=i+1,ymax=3,ls='--',color='b')


#save_path='/home/flyranch/field_data_and_analysis_scripts/2021lab/analyzed_plot_figures/'
#ex_path=save_path+date

# Check whether the specified path exists or not
#isExist = os.path.exists(ex_path)

#if not isExist:  
  # Create a new directory because it does not exist 
#    os.mkdir(ex_path)

#plt.savefig(ex_path+'/'+date+'_wind_time_plot.svg')
plt.savefig(out_path+date+'_wind_time_plot.pdf',transparent=True)


ind=new_wind_df.index[new_wind_df['time']==release[:4]].tolist()[0]

release_df=new_wind_df.iloc[[ind,ind+1,ind+2]]


print(release_df)

dir_lst=[]
spd_lst=[]
wind_dir_lst=[]
dir_calc_lst=[]
spd_calc_lst=[]
wind_dir_calc_lst=[]
for i in release_df['math_direction']:
    dir_calc_lst.append(i)
    mean_angle=np.arctan2(np.nanmean(np.sin(dir_calc_lst)),np.nanmean(np.cos(dir_calc_lst)))
    dir_lst.append(mean_angle)

for i in release_df['wind_direction']:
    wind_dir_calc_lst.append(i)
    mean_angle=np.arctan2(np.nanmean(np.sin(wind_dir_calc_lst)),np.nanmean(np.cos(wind_dir_calc_lst)))
    wind_dir_lst.append(mean_angle)    
    
for i in release_df['wind_speed']:
    spd_calc_lst.append(i)
    mean_spd=np.mean(spd_calc_lst)*0.44704
    spd_lst.append(mean_spd)
    
#print(np.rad2deg(dir_lst))
#print(dir_calc_lst)
#print(dir_lst)
#print(spd_lst)
#print(spd_calc_lst)

fig1=plt.figure(figsize=(20,10))

a=1 #number of rows
b=3 #number of columns
c=1 #plot counter

date_list11=["20240905","20240910","20240923","20241006"]
date_list12=["20240708","20240716","20240724","20240807","20240819","20240826"]
date_list8_1=["20240630"]
date_list8_2=["20230725","20230731","20230808","20231003","20231008","20231012"]
date_list8_3=["20230621","20230630"]


if date in date_list12:
    pi_loc_lst=np.arange(0,360,30)
    pi_name_lst=[10,9,8,7,6,5,4,3,2,1,12,11]

    for i in range(len(release_df)):
        ax1=plt.axes()
        ax1=plt.subplot(a,b,c, polar=True)
        ax1.set_rlim([0,2.5])
        ax1.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
        #ax1.set_rticklabels(labels=['0.5','1','1.5','2','2.5 m/s'])
        ax1.set_rlabel_position(45)


        thetaticks=np.arange(0,360,90)
        ax1.set_thetagrids(thetaticks,['E','N','W','S'])
        #ax1.set_rticklabels(["",0.5,1,1.5,2,""])
        #wind_d_theta=[dir_lst[i],dir_lst[i]]
        #ax1.plot(wind_d_theta,[0,spd_lst[i]],marker=(3,0,dir_lst[i]),markersize=10,ls='--',color='k')
        #ax1.plot(wind_d_theta,[0,spd_lst[i]],ls='-',color='k')

        #cor_x=np.cos(dir_lst[i])#*spd_lst[i]
        #cor_y=np.sin(dir_lst[i])#*spd_lst[i]
        #print(cor_x)
        #print(cor_y)
        #ax1.set_theta_zero_location('N')
        #ax1.set_theta_direction('clockwise')
        #arr1=plt.arrow(0,0,cor_x,cor_y,alpha=0.5,width=0.05,head_width=0.2,head_length=0.1,
        #             edgecolor='black',facecolor='black',lw=2,zorder=5)
        arr=plt.arrow(0,0,dir_lst[i],spd_lst[i])#,alpha=0.5,width=0.05,head_width=0.2,head_length=0.1,
                     #edgecolor='black',facecolor='black',lw=2,zorder=5)

        for n in range(len(pi_loc_lst)):
            ax1.text(np.radians(pi_loc_lst[n]),ax1.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')

        c=c+1
        
elif date in date_list11:
    pi_loc_lst=np.arange(0,360,30)
    pi_name_lst=[10,9,8,7,6,5,4,3,2,1,12,""]

    for i in range(len(release_df)):
        ax1=plt.axes()
        ax1=plt.subplot(a,b,c, polar=True)
        ax1.set_rlim([0,2.5])
        ax1.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
        #ax1.set_rticklabels(labels=['0.5','1','1.5','2','2.5 m/s'])
        ax1.set_rlabel_position(45)


        thetaticks=np.arange(0,360,90)
        ax1.set_thetagrids(thetaticks,['E','N','W','S'])
        arr=plt.arrow(0,0,dir_lst[i],spd_lst[i])

        for n in range(len(pi_loc_lst)):
            if not n==11:
                ax1.text(np.radians(pi_loc_lst[n]),ax1.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                    ha='center',va='center')

        c=c+1
        
elif date in date_list8_1:
    pi_loc_lst=np.arange(0,360,45)
    pi_name_lst=[10,6,5,4,3,2,1,8]    

    for i in range(len(release_df)):
        ax1=plt.axes()
        ax1=plt.subplot(a,b,c, polar=True)
        ax1.set_rlim([0,2.5])
        ax1.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
        ax1.set_rlabel_position(30)


        thetaticks=np.arange(0,360,90)
        ax1.set_thetagrids(thetaticks,['E','N','W','S'])

        arr=plt.arrow(0,0,dir_lst[i],spd_lst[i])

        for n in range(len(pi_loc_lst)):
            ax1.text(np.radians(pi_loc_lst[n]),ax1.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')

        c=c+1

elif date in date_list8_2:
    pi_loc_lst=np.arange(22.5,360,45)
    pi_name_lst=[2,1,8,7,6,5,4,3]    

    for i in range(len(release_df)):
        ax1=plt.axes()
        ax1=plt.subplot(a,b,c, polar=True)
        ax1.set_rlim([0,2.5])
        ax1.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
        ax1.set_rlabel_position(45)


        thetaticks=np.arange(0,360,90)
        ax1.set_thetagrids(thetaticks,['E','N','W','S'])

        arr=plt.arrow(0,0,dir_lst[i],spd_lst[i])

        for n in range(len(pi_loc_lst)):
            ax1.text(np.radians(pi_loc_lst[n]),ax1.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')

        c=c+1    

elif date in date_list8_3:
    pi_loc_lst=np.arange(22.5,360,45)
    pi_name_lst=[6,5,4,3,2,1,8,7]    

    for i in range(len(release_df)):
        ax1=plt.axes()
        ax1=plt.subplot(a,b,c, polar=True)
        ax1.set_rlim([0,2.5])
        ax1.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
        ax1.set_rlabel_position(45)


        thetaticks=np.arange(0,360,90)
        ax1.set_thetagrids(thetaticks,['E','N','W','S'])

        arr=plt.arrow(0,0,dir_lst[i],spd_lst[i])

        for n in range(len(pi_loc_lst)):
            ax1.text(np.radians(pi_loc_lst[n]),ax1.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')

        c=c+1    
            
        
plt.savefig(out_path+date+'_initial_3_mins_wind.pdf',transparent=True)







fig2,ax2=plt.subplots(figsize=(10,10),subplot_kw={'projection':'polar'})

with open('/media/flyranch/14TB_Backup/field_release/field_parameters_kh.json', 'r') as file:
    data = json.load(file)
file.close()
'''
collection_list=[]
for pi in pi_name_lst:
    if 'trap'+str(pi) in data["collections"][date].keys():
        print('trap'+str(pi))
        collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

collection_list.append(0)
#test_list=[19,30,22,16,8,4,5,11,25,24,22,0]
r_list=[2]*12
'''

if date in date_list12:
    pi_loc_lst=np.arange(0,360,30)
    pi_name_lst=[10,9,8,7,6,5,4,3,2,1,12,11]

    collection_list=[]
    for pi in pi_name_lst:
        if 'trap'+str(pi) in data["collections"][date].keys():
            print('trap'+str(pi))
            collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

    collection_list.append(0)
    #test_list=[19,30,22,16,8,4,5,11,25,24,22,0]
    r_list=[2]*12    
        
    ax2.set_rlim(0,2.5)
    ax2.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
    ax2.set_rlabel_position(45)

    thetaticks=np.arange(0,360,90)
    ax2.set_thetagrids(thetaticks,['E','N','W','S'])
    arr=plt.arrow(0,0,dir_lst[0],spd_lst[0])
    for n in range(len(pi_loc_lst)):
        plt.scatter(np.radians(pi_loc_lst[n]),r_list[n],c=collection_list[n],s=collection_list[n]*10,cmap='coolwarm',vmax=300,vmin=0)
        ax2.text(np.radians(pi_loc_lst[n]),ax2.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')
    plt.colorbar()


elif date in date_list11:
    pi_loc_lst=np.arange(0,360,30)
    pi_name_lst=[10,9,8,7,6,5,4,3,2,1,12,""]

    collection_list=[]
    for pi in pi_name_lst:
        if 'trap'+str(pi) in data["collections"][date].keys():
            print('trap'+str(pi))
            collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

    collection_list.append(0)
    #test_list=[19,30,22,16,8,4,5,11,25,24,22,0]
    r_list=[2]*12    
        
    ax2.set_rlim(0,2.5)
    ax2.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
    ax2.set_rlabel_position(45)

    thetaticks=np.arange(0,360,90)
    ax2.set_thetagrids(thetaticks,['E','N','W','S'])
    arr=plt.arrow(0,0,dir_lst[0],spd_lst[0])
    for n in range(len(pi_loc_lst)):
        plt.scatter(np.radians(pi_loc_lst[n]),r_list[n],c=collection_list[n],s=collection_list[n]*10,cmap='coolwarm',vmax=300,vmin=0)
        if not n==11:
            ax2.text(np.radians(pi_loc_lst[n]),ax2.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                     ha='center',va='center')
    plt.colorbar()

elif date in date_list8_1:
    pi_loc_lst=np.arange(0,360,45)
    pi_name_lst=[10,6,5,4,3,2,1,8]   
    collection_list=[]
    for pi in pi_name_lst:
        if 'trap'+str(pi) in data["collections"][date].keys():
            print('trap'+str(pi))
            collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

    collection_list.append(0)
    r_list=[2]*8    
        
    ax2.set_rlim(0,2.5)
    ax2.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
    ax2.set_rlabel_position(45)

    thetaticks=np.arange(0,360,90)
    ax2.set_thetagrids(thetaticks,['E','N','W','S'])
    arr=plt.arrow(0,0,dir_lst[0],spd_lst[0])
    for n in range(len(pi_loc_lst)):
        plt.scatter(np.radians(pi_loc_lst[n]),r_list[n],c=collection_list[n],s=collection_list[n]*10,cmap='coolwarm',vmax=300,vmin=0)
        ax2.text(np.radians(pi_loc_lst[n]),ax2.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')
    plt.colorbar()

elif date in date_list8_2:
    pi_loc_lst=np.arange(22.5,360,45)
    pi_name_lst=[2,1,8,7,6,5,4,3]    
    collection_list=[]
    for pi in pi_name_lst:
        if 'trap'+str(pi) in data["collections"][date].keys():
            print('trap'+str(pi))
            collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

    collection_list.append(0)
    r_list=[2]*8    
        
    ax2.set_rlim(0,2.5)
    ax2.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
    ax2.set_rlabel_position(45)

    thetaticks=np.arange(0,360,90)
    ax2.set_thetagrids(thetaticks,['E','N','W','S'])
    arr=plt.arrow(0,0,dir_lst[0],spd_lst[0])
    for n in range(len(pi_loc_lst)):
        plt.scatter(np.radians(pi_loc_lst[n]),r_list[n],c=collection_list[n],s=collection_list[n]*10,cmap='coolwarm',vmax=300,vmin=0)
        ax2.text(np.radians(pi_loc_lst[n]),ax2.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')
    plt.colorbar() 
    
elif date in date_list8_3:
    pi_loc_lst=np.arange(22.5,360,45)
    pi_name_lst=[6,5,4,3,2,1,8,7]   
    collection_list=[]
    for pi in pi_name_lst:
        if 'trap'+str(pi) in data["collections"][date].keys():
            print('trap'+str(pi))
            collection_list.append(data["collections"][date]['trap'+str(pi)]["total"])        

    collection_list.append(0)
    r_list=[2]*8    
        
    ax2.set_rlim(0,2.5)
    ax2.set_rticks([0.5,1,1.5,2,2.5],labels=['0.5','1','1.5','2','2.5 m/s'])
    ax2.set_rlabel_position(45)

    thetaticks=np.arange(0,360,90)
    ax2.set_thetagrids(thetaticks,['E','N','W','S'])
    arr=plt.arrow(0,0,dir_lst[0],spd_lst[0])
    for n in range(len(pi_loc_lst)):
        plt.scatter(np.radians(pi_loc_lst[n]),r_list[n],c=collection_list[n],s=collection_list[n]*10,cmap='coolwarm',vmax=300,vmin=0)
        ax2.text(np.radians(pi_loc_lst[n]),ax2.get_rmax()-0.15,'Pi'+str(pi_name_lst[n]),
                ha='center',va='center')
    plt.colorbar() 
    
plt.savefig(out_path+date+'_fly_collection_VS_initial_1_min_wind.pdf',transparent=True)
