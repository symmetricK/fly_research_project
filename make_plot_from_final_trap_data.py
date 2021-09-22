import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys

#f=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_output.json')
#data=json.load(f)


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
not_fly_list=[]
sec_since_release_list=[]
actual_timestamp_list=[]

for i in data['trap_'+trap]:
	for k in data['trap_'+trap][i]:
		if i=="flies on trap over time:":
			on_trap_list.append(k)
		elif i=="flies in trap over time:":
			in_trap_list.append(k)
		elif i=="not flies over time:":
			not_fly_list.append(k)
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


def calc_sec_since_release(standard,time_stamp):
	zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])
	sec=int(time_stamp[0:2])*3600+int(time_stamp[3:5])*60+int(time_stamp[6:8])
	sec_since_release=sec-zero
	return sec_since_release

for i in actual_timestamp_list:
	s=calc_sec_since_release(released_time,i)
	sec_since_release_list.append(s)


def make_accumulation_list(list):
	acc_list=[]
	for i in range(len(list)):
		ele=np.sum(list[:i+1])
		acc_list.append(ele)
	return acc_list

on_trap_acc_list=make_accumulation_list(on_trap_list)
in_trap_acc_list=make_accumulation_list(in_trap_list)
not_fly_acc_list=make_accumulation_list(not_fly_list)

# make combined list
combined_in_on_trap_list=[x+y for (x,y) in zip(on_trap_list,in_trap_list)]
combined_acc_in_on_trap_list=[x+y for (x,y) in zip(on_trap_acc_list,in_trap_acc_list)]


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,20))
fig.suptitle('Plots of Fly Data per Frame',size=30)

#ax1.plot(sec_since_release_list, on_trap_list, '-o',Markersize=6,color="r",label="on trap")
#ax1.plot(sec_since_release_list, in_trap_list, '-s',Markersize=6,color="b",label="in trap")
ax1.plot(actual_timestamp_list, on_trap_list, '-',markersize=6,color="r",label="on trap")
ax1.plot(actual_timestamp_list, in_trap_list, '-',markersize=6,color="b",label="in trap")
ax1.plot(actual_timestamp_list, combined_in_on_trap_list, '-',markersize=6,color="c",label="combined")

max_list=[]
on_trap_max_list=[]
in_trap_max_list=[]
combined_max_list=[]

for time in actual_timestamp_list:
	if time==released_time:
		m=actual_timestamp_list.index(time)
	elif time==(released_time[0:7]+str(1)):
		m=actual_timestamp_list.index(time)


#shortened list to focus on max after starting

#shortened_actual_timestamp_list=actual_timestamp_list[m:len(actual_timestamp_list)]
#shortened_on_trap_list=on_trap_list[m:len(on_trap_list)]
#shortened_in_trap_list=in_trap_list[m:len(in_trap_list)]
#shortened_combined_in_on_trap_list=combined_in_on_trap_list[m:len(combined_in_on_trap_list)]

shortened_actual_timestamp_list=actual_timestamp_list[m:-1-90]
shortened_on_trap_list=on_trap_list[m:-1-90]
shortened_in_trap_list=in_trap_list[m:-1-90]
shortened_combined_in_on_trap_list=combined_in_on_trap_list[m:-1-90]

for i in range(len(shortened_actual_timestamp_list)):
	if np.max(shortened_on_trap_list)==shortened_on_trap_list[i]:
		if len(on_trap_max_list)==0:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_on_trap_list[i],'o',markersize=10,color="r",label="on trap max")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies on trap: '+str(int(shortened_on_trap_list[i])))
		else:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_on_trap_list[i],'o',markersize=10,color="r")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies on trap: '+str(int(shortened_on_trap_list[i])))		
		on_trap_max_list.append(shortened_actual_timestamp_list[i])	
	if np.max(shortened_in_trap_list)==shortened_in_trap_list[i]:
		if len(in_trap_max_list)==0:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_in_trap_list[i],'s',markersize=10,color="b",label="in trap max")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in trap: '+str(int(shortened_in_trap_list[i])))
		else:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_in_trap_list[i],'s',markersize=10,color="b")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in trap: '+str(int(shortened_in_trap_list[i])))
		in_trap_max_list.append(shortened_actual_timestamp_list[i])
	if np.max(shortened_combined_in_on_trap_list)==shortened_combined_in_on_trap_list[i]:
		if len(combined_max_list)==0:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_combined_in_on_trap_list[i],'^',markersize=10,color="c",label="combined max")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in total: '+str(int(shortened_combined_in_on_trap_list[i])))
		else:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_combined_in_on_trap_list[i],'^',markersize=10,color="c")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in total: '+str(int(shortened_combined_in_on_trap_list[i])))			
		combined_max_list.append(shortened_actual_timestamp_list[i])



max_list=on_trap_max_list+in_trap_max_list+combined_max_list

for i in max_list:
	for j in actual_timestamp_list:
		if i==j:
			print(actual_timestamp_list.index(j))
			ax1.annotate('max',xy=(actual_timestamp_list[actual_timestamp_list.index(j)],np.max(combined_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
			ax1.axvline(actual_timestamp_list[actual_timestamp_list.index(j)],ymax=np.max(combined_in_on_trap_list),ls='--')
max_list.extend((actual_timestamp_list[0],actual_timestamp_list[m],actual_timestamp_list[-1],actual_timestamp_list[-1-90]))
max_list=list(set(max_list))


ax1.annotate('released',xy=(actual_timestamp_list[m],np.max(combined_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
ax1.axvline(actual_timestamp_list[m],ymax=np.max(combined_in_on_trap_list),ls='--')
ax1.annotate('end',xy=(actual_timestamp_list[-1-90],np.max(combined_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
ax1.axvline(actual_timestamp_list[-1-90],ymax=np.max(combined_in_on_trap_list),ls='--')

ax1.set_xticks(max_list)
ax1.set_xticklabels(max_list,rotation=45,size=10)
ax1.set_xlabel('timestamp',size=24)
ax1.set_ylabel('number of flies in a frame',size=24)
ax1.legend(loc="upper left",fontsize=14)


xtick_list=[]
before_release_list=sec_since_release_list[0:m+1][::-30]
after_release_list=sec_since_release_list[m:-1][::30]
xtick_list=before_release_list+after_release_list
xtick_list.append(sec_since_release_list[0])
xtick_list.append(sec_since_release_list[-1])
xtick_list.sort()
xtick_list_dup_removed=[]
for i in xtick_list:
	if i not in xtick_list_dup_removed:
		xtick_list_dup_removed.append(i)



ax2.annotate('released',xy=(sec_since_release_list[m],np.max(combined_acc_in_on_trap_list,)),bbox=dict(boxstyle="round",fc="0.8"))
ax2.axvline(sec_since_release_list[m],ymax=np.max(combined_acc_in_on_trap_list,),ls='--')
ax2.annotate('end',xy=(sec_since_release_list[-1-90],np.max(combined_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
ax2.axvline(sec_since_release_list[-1-90],ymax=np.max(combined_in_on_trap_list),ls='--')

ax2.plot(sec_since_release_list, on_trap_acc_list, '-',markersize=6,color="r",label="on trap")
ax2.plot(sec_since_release_list, in_trap_acc_list, '-',markersize=6,color="b",label="in trap")
ax2.plot(sec_since_release_list, combined_acc_in_on_trap_list, '-',markersize=6,color="c",label="combined")
ax2.set_xticks(xtick_list_dup_removed)
ax2.set_xticklabels(xtick_list_dup_removed,rotation=45,size=10)
ax2.set_xlabel('seconds since released',size=24)
ax2.set_ylabel('total number of flies',size=24)
ax2.legend(loc="upper left",fontsize=14)


plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/trap_'+trap+'_videos/flies_time.jpg')
