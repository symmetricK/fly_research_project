import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys

#ask user input
trap=input("Enter a trap letter to analyze: ")


f=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap+'/master_trap_'+trap+'.json')
data=json.load(f)


release=input("What time flies were released? (e.g. 093425) :")
if (len(release)==6 and type(int(release))==int):
	pass
else:
	print("please enter 6 numbers (000000-235959)")
	sys.exit()

released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]

#create lists
on_trap_list=[]
in_trap_list=[]
sec_since_release_list=[]
actual_timestamp_list=[]

for i in data['trap_'+trap]:
	for k in data['trap_'+trap][i]:
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


def calc_sec_since_release(standard,time_stamp):
	zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])+1
	sec=int(time_stamp[0:2])*3600+int(time_stamp[3:5])*60+int(time_stamp[6:8])
	sec_since_release=sec-zero
	return sec_since_release

for i in actual_timestamp_list:
	s=calc_sec_since_release(released_time,i)
	if s>0:
		sec_since_release_list.append(s)

min_since_release_list=[]

for i in sec_since_release_list:
	m=int(i/60)
	min_since_release_list.append(m)


ind=0

fig=plt.figure()
plt.xlim(0,950)
plt.ylim(0,16)
plt.xlabel('time since release (min)')
plt.ylabel('flies on trap')


for i in range(len(min_since_release_list[:450])):
	plt.plot(min_since_release_list[:i], on_trap_list[:i], '-',markersize=6,color="r",label="on trap")

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,20))

x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_plots_figures/Cate/trap_'+trap+'_plots_on_only.png')


