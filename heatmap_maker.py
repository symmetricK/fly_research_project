import seaborn as sns
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys
import glob
import os
import re
import pandas as pd
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline

matplotlib.rcParams['pdf.fonttype'] = 42


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



date=input("what date data you wanna use to make the plot (e.g. 20220725): ")
#date='20240923'
release=input("What time flies were released? (e.g. 093425) :")
#release='082010'
if (len(release)==6 and type(int(release))==int):
	pass
else:
	print("please enter 6 numbers (000000-235959)")
	sys.exit()

path='/media/flyranch/14TB_Backup/field_release/'
json_path=path+'all_traps_final_analysis_json_files/'
list_of_files=sorted(glob.glob(json_path+date+'/*/master_*.json'))

released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]

#c=0

with open(path+'wind_direction.json', 'r') as file:
    data = json.load(file)
file.close()

upwind_list=data["wind_direction"][date]["upwind"]
downwind_list=data["wind_direction"][date]["downwind"]
Color=''

Heat_lst=[]
Trap_name_lst=[]

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
    match=(re.search(pattern,string))
    
    j_pattern='.json'
    j_match=(re.finditer(j_pattern,string))
    count=0
    for i in j_match:
        if count==1:
            jj_match=i
        count+=1
    
    END=match.end()
    START=jj_match.start()
    DIFF=START-END
    
    if DIFF==24:
        trap_name=string[match.end()+6:-5] ###remove 'master_trap_' and '.json'
        t_name=string[match.end()+6:match.end()+9] ###Pi_X
    else:
        trap_name=string[match.end()+6:-5] ###remove 'master_trap_' and '.json'
        t_name=string[match.end()+6:match.end()+10] ###Pi_X
    #print(t_name[2:])

    for i in data['trap_'+trap_name]:
        for k in data['trap_'+trap_name][i]:
            if i=="flies on trap over time:":
                on_trap_list.append(k)
            elif i=="flies in trap over time:":
                in_trap_list.append(k)
    #		elif i=="seconds since release:":
    #			sec_since_release_list.append(int(k))
            elif i=="actual timestamp:":
                if len(str(int(k)))==5:
                    str_time='0'+str(int(k))[0:1]+':'+str(int(k))[1:3]+':'+str(int(k))[3:5]
                    actual_timestamp_list.append(str_time)
                elif len(str(int(k)))==6:
                    str_time=str(int(k))[0:2]+':'+str(int(k))[2:4]+':'+str(int(k))[4:6]
                    actual_timestamp_list.append(str_time)

    f.close()

    for i in actual_timestamp_list:
        s=calc_sec_since_release(released_time,i)
        sec_since_release_list.append(s)

    on_trap_acc_list=make_accumulation_list(on_trap_list)
    in_trap_acc_list=make_accumulation_list(in_trap_list)

    Heat_lst.append(on_trap_list)
    Trap_name_lst.append(t_name)


fig,ax=plt.subplots(figsize=(18,9))

sorted_Heat_lst=[]
sorted_Trap_name_lst=sorted(Trap_name_lst,key=len)
#print(sorted_Trap_name_lst)
for i in sorted_Trap_name_lst:
    for j in Trap_name_lst:
        if i==j:
            ind=Trap_name_lst.index(j)
            sorted_Heat_lst.append(Heat_lst[ind])

for name in sorted_Trap_name_lst:
    if int(name[2:]) in upwind_list:
        print(sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]+'\nUPwind')
        sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]=sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]+'\nUPwind'
    elif int(name[2:]) in downwind_list:
        print(sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]+'\nDOWNwind')
        sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]=sorted_Trap_name_lst[sorted_Trap_name_lst.index(name)]+'\nDOWNwind'

    
sorted_heat_df=pd.DataFrame(sorted_Heat_lst,index=sorted_Trap_name_lst)
hm=sns.heatmap(data=sorted_heat_df,linewidths=0.0,rasterized=True,
    cbar_kws={"label":"Flies on Trap"}) 

ax.set_xticks(np.arange(0,len(sorted_Heat_lst[0])+1,60))
ax.set_xticklabels(np.arange(-3,int(((len(sorted_Heat_lst[0])/60)-3+1)),1),rotation=0) ###3 mins before release + 30mins after release
ax.axvline(180,c="g",lw=3)
ax.set_xlabel('minutes since release')
ax.set_ylabel('Pi Camera Number')
ax.set_title(date+" Flies on Trap by Time ",fontsize=20)

out_path=path+'analyzed_plot_figures/'
ex_path=out_path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.makedirs(ex_path)

plt.savefig(ex_path+'/'+date+'_heatmap.pdf',transparent=True)