import json
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

def make_upwind_downwind_group(num1,num2):
	if (num1==1 and num2==8) or (num1==8 and num2==1):
		num1=8
		num2=1
	elif num1>num2:
		num1=num2
		num2=num2+1
	trap_num_list=[1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
	upwind1=[]
	upwind2=[]
	downwind2=[]
	downwind1=[]
	for ind,ele in enumerate(trap_num_list):
		if (4<=ind<len(trap_num_list)-4) and ele==num1:
			upwind1.append((ele,trap_num_list[ind+1]))
			upwind2.append((trap_num_list[ind-1],trap_num_list[ind+2]))    
			downwind2.append((trap_num_list[ind-2],trap_num_list[ind+3]))
			downwind1.append((trap_num_list[ind-3],trap_num_list[ind+4]))
	wind_dict={'upwind++':upwind1,'upwind+':upwind2,'downwind+':downwind2,'downwind++':downwind1}
	return wind_dict




path='/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/'
date=input("what date data you wanna use to make the plot (e.g. 20220725): ")
list_of_files= sorted(glob.glob(path+date+'/*/master_*.json'))


release=input("What time flies were released? (e.g. 093425) :")
if (len(release)==6 and type(int(release))==int):
	pass
else:
	print("please enter 6 numbers (000000-235959)")
	sys.exit()

released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]

a=input("Enter a trap number located in upwind (e.g. 4) :")
b=input("Enter another trap number located in upwind (e.g. 5) :")

w_dict=make_upwind_downwind_group(int(a),int(b))
#print(w_dict)


colors=['']*8

for key,val in w_dict.items():
	if key=='upwind++':
		colors[val[0][0]-1]='r'
		colors[val[0][1]-1]='r'
	elif key=='upwind+':
		colors[val[0][0]-1]='m'
		colors[val[0][1]-1]='m'
	elif key=='downwind+':
		colors[val[0][0]-1]='c'
		colors[val[0][1]-1]='c'
	elif key=='downwind++':
		colors[val[0][0]-1]='b'
		colors[val[0][1]-1]='b'

#print(colors)
c=0

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,20))
fig.suptitle(date+' All Trap Data for Ontrap',size=30)
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
	match=(re.search(pattern, string))

	trap_name=string[match.end()+6:-5] ###remove 'master_trap_' and '.json'
	t_name=string[match.end()+6:match.end()+9] ###Pi_X
	#pdb.set_trace()

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



	
	#ax1.plot(sec_since_release_list, on_trap_list, '-',markersize=6,label='trap_'+trap_name)
	#ax2.plot(actual_timestamp_list, in_trap_list, '-',markersize=6,color="b",label="in trap")
	#ax1.legend(loc="upper right",fontsize=14)

	###to smooth line plots
	cubic_interploation_model = interp1d(sec_since_release_list, on_trap_list, kind = "cubic")
	X_Y_Spline = make_interp_spline(sec_since_release_list, on_trap_list)
	# Plotting the Graph
	X_=np.linspace(np.array(sec_since_release_list).min(), np.array(sec_since_release_list).max(), 500)
	#Y_=cubic_interploation_model(X_)
	Y_=X_Y_Spline(X_)

	if colors[c]=='r':
		wind_dir='upwind++'
	elif colors[c]=='m':
		wind_dir='upwind+'
	elif colors[c]=='c':
		wind_dir='downwind+'
	elif colors[c]=='b':
		wind_dir='downwind++'

	#ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')',color=colors[c])
	ax1.plot(X_,Y_,'-',markersize=6,linewidth=2,label=t_name+'('+wind_dir+')')
	ax1.legend(loc="upper right",fontsize=14)
	ax1.set_xlabel('seconds since released',size=24)
	ax1.set_ylabel('number of flies in a frame',size=24)

	ax2.plot(sec_since_release_list,on_trap_acc_list,'-',markersize=6,linewidth=4,label=t_name+'('+wind_dir+')',color=colors[c])
	ax2.annotate(t_name,(sec_since_release_list[-1]+50,on_trap_acc_list[-1]+50))
	ax2.legend(loc="upper left",fontsize=14)
	ax2.set_xlabel('seconds since released',size=24)
	ax2.set_ylabel('total number of flies',size=24)

	c+=1


data_path='/home/flyranch/field_data_and_analysis_scripts/2021lab/analyzed_plot_figures/'
ex_path=data_path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.mkdir(ex_path)



plt.savefig(ex_path+'/all_on_trap_data_plot.jpg')