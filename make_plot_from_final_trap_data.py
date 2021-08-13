import json
import matplotlib.pyplot as plt
import numpy as np
import pdb

f=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_output.json')
data=json.load(f)

on_trap_list=[]
in_trap_list=[]
sec_since_release_list=[]

#ask user input
trap=input("Enter a trap letter to analyze: ")

for i in data['trap_'+trap]:
	for k in data['trap_'+trap][i]:
		if i=="flies on trap over time:":
			on_trap_list.append(k)
		elif i=="flies in trap over time:":
			in_trap_list.append(k)
		elif i=="seconds since release:":
			sec_since_release_list.append(k)

f.close()

def make_accumulation_list(list):
	acc_list=[]
	for i in range(len(list)):
		ele=np.sum(list[:i+1])
		acc_list.append(ele)
	return acc_list

on_trap_acc_list=make_accumulation_list(on_trap_list)
in_trap_acc_list=make_accumulation_list(in_trap_list)


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(15,15))
fig.suptitle('Plots of Fly Data per Frame',size=30)




ax1.plot(sec_since_release_list, on_trap_list, '-o',Markersize=6,color="r",label="on trap")
ax1.plot(sec_since_release_list, in_trap_list, '-s',Markersize=6,color="b",label="in trap")
#ax1.set_xlabel('seconds_since_released')
ax1.set_ylabel('number of flies in frame',size=24)
ax1.legend(loc="upper left",fontsize=24)

ax2.plot(sec_since_release_list, on_trap_acc_list, '-o',Markersize=6,color="r",label="on trap")
ax2.plot(sec_since_release_list, in_trap_acc_list, '-s',Markersize=6,color="b",label="in trap")
ax2.set_xlabel('seconds since released',size=24)
ax2.set_ylabel('total number of flies',size=24)
ax2.legend(loc="upper left",fontsize=24)

plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/trap_'+trap+'_videos/flies_time.jpg')
