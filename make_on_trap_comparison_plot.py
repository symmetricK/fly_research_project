## from math import radians
import matplotlib.pyplot as plt
import numpy as np
import pdb
import time
import datetime
import sys
import json

#2 traps
trap_I='2021_10_30_I'
trap_J='2021_10_30_J'

f_I=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap_I+'/master_trap_'+trap_I+'.json')
data_I=json.load(f_I)
f_J=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap_J+'/master_trap_'+trap_J+'.json')
data_J=json.load(f_J)

release='142000'
released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]

#create lists
on_trap_list_I=[]
in_trap_list_I=[]
sec_since_release_list_I=[]
actual_timestamp_list_I=[]

on_trap_list_J=[]
in_trap_list_J=[]
sec_since_release_list_J=[]
actual_timestamp_list_J=[]

for i in data_I['trap_'+trap_I]:
	for k in data_I['trap_'+trap_I][i]:
		if i=="flies on trap over time:":
			on_trap_list_I.append(k)
		elif i=="flies in trap over time:":
			in_trap_list_I.append(k)
		elif i=="actual timestamp:":
			if len(str(int(k)))==5:
				str_time='0'+str(int(k))[0:1]+':'+str(int(k))[1:3]+':'+str(int(k))[3:5]
				actual_timestamp_list_I.append(str_time)
			elif len(str(int(k)))==6:
				str_time=str(int(k))[0:2]+':'+str(int(k))[2:4]+':'+str(int(k))[4:6]
				actual_timestamp_list_I.append(str_time)

for i in data_J['trap_'+trap_J]:
	for k in data_J['trap_'+trap_J][i]:
		if i=="flies on trap over time:":
			on_trap_list_J.append(k)
		elif i=="flies in trap over time:":
			in_trap_list_J.append(k)                
		elif i=="actual timestamp:":
			if len(str(int(k)))==5:
				str_time='0'+str(int(k))[0:1]+':'+str(int(k))[1:3]+':'+str(int(k))[3:5]
				actual_timestamp_list_J.append(str_time)
			elif len(str(int(k)))==6:
				str_time=str(int(k))[0:2]+':'+str(int(k))[2:4]+':'+str(int(k))[4:6]
				actual_timestamp_list_J.append(str_time)
                        
f_I.close()
f_J.close()

def calc_sec_since_release(standard,time_stamp):
	zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])+1
	sec=int(time_stamp[0:2])*3600+int(time_stamp[3:5])*60+int(time_stamp[6:8])
	sec_since_release=sec-zero
	return sec_since_release

for i in actual_timestamp_list_I:
	s=calc_sec_since_release(released_time,i)
	sec_since_release_list_I.append(s)

for i in actual_timestamp_list_J:
	s=calc_sec_since_release(released_time,i)
	sec_since_release_list_J.append(s)


def make_accumulation_list(list):
	acc_list=[]
	for i in range(len(list)):
		ele=np.sum(list[:i+1])
		acc_list.append(ele)
	return acc_list

on_trap_acc_list=make_accumulation_list(on_trap_list_I)
in_trap_acc_list=make_accumulation_list(in_trap_list_I)


fig2=plt.figure(figsize=(15,10))
ax2=plt.axes()
sec_since_release_list_I_20min=[]
on_trap_list_I_20min=[]
sec_since_release_list_J_20min=[]
on_trap_list_J_20min=[]

for i in sec_since_release_list_I:
    if 0<=i<1201:
#        print(on_trap_list_I[sec_since_release_list_I.index(i)])
        x=i
        y=on_trap_list_I[sec_since_release_list_I.index(i)]
        sec_since_release_list_I_20min.append(x)
        on_trap_list_I_20min.append(y)
for i in sec_since_release_list_J:
    if 0<=i<1201:
#        print(on_trap_list_J[sec_since_release_list_J.index(i)])
        x=i
        y=on_trap_list_J[sec_since_release_list_J.index(i)]
        sec_since_release_list_J_20min.append(x)
        on_trap_list_J_20min.append(y)
ax2.plot(sec_since_release_list_I_20min,on_trap_list_I_20min,markersize=6,color="r",label="on trap I (upwind)")
ax2.plot(sec_since_release_list_J_20min,on_trap_list_J_20min,markersize=6,color="b",label="on trap J (downwind)")
ax2.legend()
ax2.set_xlabel('time(sec)')
ax2.set_ylabel('number of flies on trap')


path="/home/flyranch/field_data_and_analysis_scripts/2021lab/refs_for_presentation/"


plt.savefig(path+"upwind_downwind_on_trap_comparison.svg")

#print(sec_since_release_list_I_5min)

#print(sec_since_release_list_J_5min)

