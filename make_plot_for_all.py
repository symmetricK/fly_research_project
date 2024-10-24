import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys
import glob
import os
import re
from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline


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
#date='20241006'
release=input("What time flies were released? (e.g. 093425) :")
#release='101551'
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
matplotlib.rcParams['pdf.fonttype'] = 42

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,20))
fig.suptitle(date+' All Trap Data for Ontrap',size=30,x=0.5,y=0.95)
x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)
y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

#pdb.set_trace()

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



    #print(on_trap_acc_list)
    #print(Y_)
    #print(sec_since_release_list)


    #ax1.plot(sec_since_release_list, on_trap_list, '-',markersize=6,label='trap_'+trap_name)
    #ax2.plot(actual_timestamp_list, in_trap_list, '-',markersize=6,color="b",label="in trap")
    #ax1.legend(loc="upper right",fontsize=14)

    ###to smooth line plots
    #cubic_interploation_model = interp1d(sec_since_release_list, on_trap_list, kind = "cubic")
    #X_Y_Spline = make_interp_spline(sec_since_release_list, on_trap_list)
    # Plotting the Graph
    #X_=np.linspace(np.array(sec_since_release_list).min(), np.array(sec_since_release_list).max(), 500)
    #Y_=cubic_interploation_model(X_)
    #Y_=X_Y_Spline(X_)

    #for i in range(len(w_lst)):
    #    if w_lst[i][0][0]==int(t_name[-1]):
    
    if int(t_name[2:]) in upwind_list:
        Color='r'
        ax1.plot(sec_since_release_list,on_trap_list,'-',markersize=6,linewidth=2,label=t_name+' (upwind)',color=Color)
        ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name+' (upwind)',color=Color)
        ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
    elif int(t_name[2:]) in downwind_list:
        Color='b'
        ax1.plot(sec_since_release_list,on_trap_list,'-',markersize=6,linewidth=2,label=t_name+' (downwind)',color=Color)
        ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name+' (downwind)',color=Color)
        ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
    else:
        Color='c'
        ax1.plot(sec_since_release_list,on_trap_list,'-',markersize=6,linewidth=2,label=t_name,color=Color)
        ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name,color=Color)
        ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
    #print(Color)
    #ax1.plot(sec_since_release_list,on_trap_list,'-',markersize=6,linewidth=2,label=t_name,color=Color)
    #ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')')
    ax1.legend(loc="upper right",fontsize=14)
    ax1.set_xlabel('seconds since released',size=24)
    ax1.set_ylabel('number of flies in a frame',size=24)

    #ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name,color=Color)
    #ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
    ax2.legend(loc="upper left",fontsize=14)
    ax2.set_xlabel('seconds since released',size=24)
    ax2.set_ylabel('total number of flies',size=24)

'''
        elif w_lst[i][0][1]==int(t_name[-1]):
            ax1.plot(X_,Y_,'--',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')',color=colors[c])
            #ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')')
            ax1.legend(loc="upper right",fontsize=14)
            ax1.set_xlabel('seconds since released',size=24)
            ax1.set_ylabel('number of flies in a frame',size=24)


            ax2.plot(sec_since_release_list,on_trap_acc_list,'--',markersize=6,linewidth=4,label=t_name+'('+wind_dir+')',color=colors[c])
            ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
            ax2.legend(loc="upper left",fontsize=14)
            ax2.set_xlabel('seconds since released',size=24)
            ax2.set_ylabel('total number of flies',size=24)
'''

    #ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')',color=colors[c])
    #ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')')
    #ax1.legend(loc="upper right",fontsize=14)
    #ax1.set_xlabel('seconds since released',size=24)
    #ax1.set_ylabel('number of flies in a frame',size=24)

    #ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name+'('+wind_dir+')',color=colors[c])
    #ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
    #ax2.legend(loc="upper left",fontsize=14)
    #ax2.set_xlabel('seconds since released',size=24)
    #ax2.set_ylabel('total number of flies',size=24)

    #c+=1


out_path=path+'analyzed_plot_figures/'
ex_path=out_path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.makedirs(ex_path)

plt.savefig(ex_path+'/'+date+'_all_on_trap_data_plot.pdf',transparent=True)