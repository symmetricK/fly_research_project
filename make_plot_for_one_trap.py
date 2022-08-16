import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys
import os



def time_converter(timestamp):
	### convert time stamp to seconds
	sec=int(timestamp[:2])*3600+int(timestamp[3:5])*60+int(timestamp[6:8])
	return sec


#ask user input
trap=input("Enter a trap name you would like to make plots without (trap_): ")
date=input("what date did you release flies (e.g. 20220725): ")

f=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/'+date+'/trap_'+trap+'/master_trap_'+trap+'.json')
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
	zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])+1
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

#n_fly=input("You want to see excluded by contour data on the plot? (y or n): ")
n_fly='n'
x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(20,20))
#fig.suptitle('Plots of Fly Data per Frame: trap_'+trap+ '\n Released Time: '+released_time,size=30)
if n_fly=="y":
	fig.suptitle('Plots of Fly Data per Frame with Not Fly Data: trap_'+trap,size=30)
if n_fly=="n":
	fig.suptitle('Plots of Fly Data per Frame: trap_'+trap,size=30)



#ax1.plot(sec_since_release_list, on_trap_list, '-o',Markersize=6,color="r",label="on trap")
#ax1.plot(sec_since_release_list, in_trap_list, '-s',Markersize=6,color="b",label="in trap")
ax1.plot(actual_timestamp_list, on_trap_list, '-',markersize=6,color="r",label="on trap")
ax1.plot(actual_timestamp_list, in_trap_list, '-',markersize=6,color="b",label="in trap")
#ax1.plot(actual_timestamp_list, combined_in_on_trap_list, '-',markersize=6,color="c",label="combined")
if n_fly=="y":
	ax1.plot(actual_timestamp_list, not_fly_list, '-',markersize=6,color="m",label="not fly")

max_list=[]
on_trap_max_list=[]
in_trap_max_list=[]
combined_max_list=[]

for time in actual_timestamp_list:
#	pdb.set_trace()
	if time==released_time:
		m=actual_timestamp_list.index(time)
	elif (int(time[0:2])*3600+int(time[3:5])*60+int(time[6:8]))==(int(released_time[0:2])*3600+int(released_time[3:5])*60+int(released_time[6:8])+1):
		m=actual_timestamp_list.index(time)
	elif (int(time[0:2])*3600+int(time[3:5])*60+int(time[6:8]))==(int(released_time[0:2])*3600+int(released_time[3:5])*60+int(released_time[6:8])-1):
		m=actual_timestamp_list.index(time)


'''
	elif time[6:8]=='00':
		if time[3:5]=='00':
			if int(time[0:2])<=10:
				print('b')
				time='0'+str(int(time[0:2])-1)+':59:59'
				m=actual_timestamp_list.index(time)
				print('c')
				time=str(int(time[0:2])-1)+':59:59'
				m=actual_timestamp_list.index(time)
		else:
			if int(time[3:5])<=10:
				print('d')
				time=time[0:2]+':0'+str(int(time[3:5])-1)+':59'
				m=actual_timestamp_list.index(time)
			else:
				print('e')
				time=time[0:2]+':'+str(int(time[3:5])-1)+':59'
				m=actual_timestamp_list.index(time)
'''


#	str(int(time[0:2]+time[3:5]+time[6:8]))[4:6]=='00'
#
#	elif str(int(time[0:2]+time[3:5]+time[6:8])+1)[0:2]+':'+str(int(time[0:2]+time[3:5]+time[6:8])+1)[2:4]+':'+str(int(time[0:2]+time[3:5]+time[6:8])-1)[4:6]==released_time:
#		m=actual_timestamp_list.index(time)


#pdb.set_trace()
#cut=input("You want to cut last three minutes data?(y or n): ")
cut='n'
#shortened list to focus on max after starting
if cut=='y':
	shortened_actual_timestamp_list=actual_timestamp_list[m:-1-90]
	shortened_on_trap_list=on_trap_list[m:-1-90]
	shortened_in_trap_list=in_trap_list[m:-1-90]
	shortened_combined_in_on_trap_list=combined_in_on_trap_list[m:-1-90]
else:
	shortened_actual_timestamp_list=actual_timestamp_list[m:len(actual_timestamp_list)]
	shortened_on_trap_list=on_trap_list[m:len(on_trap_list)]
	shortened_in_trap_list=in_trap_list[m:len(in_trap_list)]
	shortened_combined_in_on_trap_list=combined_in_on_trap_list[m:len(combined_in_on_trap_list)]

nonzero_ind=[idx for idx, val in enumerate(shortened_on_trap_list) if val != 0]
travel_time=time_converter(shortened_actual_timestamp_list[nonzero_ind[0]])-time_converter(shortened_actual_timestamp_list[0])
First='frame '+shortened_actual_timestamp_list[nonzero_ind[0]][0:2]+shortened_actual_timestamp_list[nonzero_ind[0]][3:5]+shortened_actual_timestamp_list[nonzero_ind[0]][6:8]+' has the first on trap fly: travel time is '+str(travel_time)+' sec'
#print('frame '+shortened_actual_timestamp_list[nonzero_ind[0]][0:2]+shortened_actual_timestamp_list[nonzero_ind[0]][3:5]+shortened_actual_timestamp_list[nonzero_ind[0]][6:8]+' has the first on trap flies: travel time is '+str(travel_time))
print(First)
Peak=''
for i in range(len(shortened_actual_timestamp_list)):
	if np.max(shortened_on_trap_list)==shortened_on_trap_list[i]:
		if len(on_trap_max_list)==0:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_on_trap_list[i],'o',markersize=10,color="r",label="on trap max")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies on trap: '+str(int(shortened_on_trap_list[i])))
		else:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_on_trap_list[i],'o',markersize=10,color="r")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies on trap: '+str(int(shortened_on_trap_list[i])))		
		Peak='frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies on trap: '+str(int(shortened_on_trap_list[i]))
		on_trap_max_list.append(shortened_actual_timestamp_list[i])	
	if np.max(shortened_in_trap_list)==shortened_in_trap_list[i]:
		if len(in_trap_max_list)==0:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_in_trap_list[i],'s',markersize=10,color="b",label="in trap max")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in trap: '+str(int(shortened_in_trap_list[i])))
		else:
			ax1.plot(shortened_actual_timestamp_list[i],shortened_in_trap_list[i],'s',markersize=10,color="b")
			print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in trap: '+str(int(shortened_in_trap_list[i])))
		in_trap_max_list.append(shortened_actual_timestamp_list[i])
	#if np.max(shortened_combined_in_on_trap_list)==shortened_combined_in_on_trap_list[i]:
	#	if len(combined_max_list)==0:
	#		ax1.plot(shortened_actual_timestamp_list[i],shortened_combined_in_on_trap_list[i],'^',markersize=10,color="c",label="combined max")
	#		print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in total: '+str(int(shortened_combined_in_on_trap_list[i])))
	#	else:
	#		ax1.plot(shortened_actual_timestamp_list[i],shortened_combined_in_on_trap_list[i],'^',markersize=10,color="c")
	#		print('frame '+shortened_actual_timestamp_list[i][0:2]+shortened_actual_timestamp_list[i][3:5]+shortened_actual_timestamp_list[i][6:8]+' has the most flies in total: '+str(int(shortened_combined_in_on_trap_list[i])))			
	#	combined_max_list.append(shortened_actual_timestamp_list[i])



max_list=on_trap_max_list+in_trap_max_list+combined_max_list


for i in max_list:
	for j in actual_timestamp_list:
		if i==j:
			ax1.annotate('max',xy=(actual_timestamp_list[actual_timestamp_list.index(j)],np.max(combined_in_on_trap_list)-10),bbox=dict(boxstyle="round",fc="0.8"))
			ax1.axvline(actual_timestamp_list[actual_timestamp_list.index(j)],ymax=np.max(combined_in_on_trap_list),ls='--')

if cut=='y':
	max_list.extend((actual_timestamp_list[0],actual_timestamp_list[m],actual_timestamp_list[-1],actual_timestamp_list[-1-90]))
elif cut=='n':
	max_list.extend((actual_timestamp_list[0],actual_timestamp_list[m],actual_timestamp_list[-1]))

max_list=list(set(max_list))


ax1.annotate('released',xy=(actual_timestamp_list[m],np.max(combined_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
ax1.axvline(actual_timestamp_list[m],ymax=np.max(combined_in_on_trap_list),ls='--')

if cut=='y':
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

sec_max_list=[]

max_list.remove(actual_timestamp_list[0])
max_list.remove(actual_timestamp_list[m])
max_list.remove(actual_timestamp_list[-1])
if cut=='y':
	max_list.remove(actual_timestamp_list[-1-90])
for i in max_list:
	sec_max_list.append(sec_since_release_list[actual_timestamp_list.index(i)])

for i in sec_max_list:
	ax2.annotate(str(i),xy=(sec_max_list[sec_max_list.index(i)],np.max(combined_acc_in_on_trap_list)-200),bbox=dict(boxstyle="round",fc="0.8"))
	ax2.axvline(sec_max_list[sec_max_list.index(i)],ymax=np.max(combined_acc_in_on_trap_list),ls='--')

ax2.annotate('released',xy=(sec_since_release_list[m],np.max(combined_acc_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
ax2.axvline(sec_since_release_list[m],ymax=np.max(combined_acc_in_on_trap_list,),ls='--')

if cut=='y':
	ax2.annotate('end',xy=(sec_since_release_list[-1-90],np.max(combined_acc_in_on_trap_list)),bbox=dict(boxstyle="round",fc="0.8"))
	ax2.axvline(sec_since_release_list[-1-90],ymax=np.max(combined_acc_in_on_trap_list),ls='--')

ax2.plot(sec_since_release_list, on_trap_acc_list, '-',markersize=6,color="r",label="on trap")
ax2.plot(sec_since_release_list, in_trap_acc_list, '-',markersize=6,color="b",label="in trap")
#ax2.plot(sec_since_release_list, combined_acc_in_on_trap_list, '-',markersize=6,color="c",label="combined")
if n_fly=="y":
	ax2.plot(sec_since_release_list, not_fly_acc_list, '-',markersize=6,color="m",label="not fly")

xtick_list_dup_removed.extend(sec_max_list)

ax2.set_xticks(xtick_list_dup_removed)
ax2.set_xticklabels(xtick_list_dup_removed,rotation=45,size=10)
ax2.set_xlabel('seconds since released',size=24)
ax2.set_ylabel('total number of flies',size=24)
ax2.legend(loc="upper left",fontsize=14)

path='/home/flyranch/field_data_and_analysis_scripts/2021lab/analyzed_plot_figures/'
ex_path=path+date

# Check whether the specified path exists or not
isExist = os.path.exists(ex_path)

if not isExist:  
  # Create a new directory because it does not exist 
    os.mkdir(ex_path)

if n_fly=="y":
	plt.savefig(ex_path+'/trap_'+trap+'_with_not_fly_plots.jpg')
if n_fly=="n":
	plt.savefig(ex_path+'/trap_'+trap+'_plots.jpg')
