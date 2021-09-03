import json
import matplotlib.pyplot as plt
import numpy as np
import pdb


def remove_trapname(dict1,key):
	'''remove trap_name to merge two dicts'''
	dict2=dict1[key]
	return dict2


def merge_dict(dict3, dict4):
	''' Merge dictionaries and keep values of common keys in list'''
	dict5 = {**dict3, **dict4}
	for key, value in dict5.items():
		if key in dict3 and key in dict4:
			dict5[key] = [value , dict3[key]]

	duplicate_index_list=[]
	for key, value in dict5.items():
		if key=='actual timestamp:':
			for i in value[0]:
				for j in value[1]:
					if j==i:
						duplicate_index_list.append(value[0].index(i))			

	start=duplicate_index_list[0]
	end=duplicate_index_list.pop()
	

	for value in dict5.values():
		del value[0][start:end+1]

	dict6={}

	for key in dict5.keys():
		if key=='actual timestamp:':
			for key,value in dict5.items():
				if value[0][0]>value[1][0]:
					value=value[1]+value[0]
					
				elif value[0][0]<value[1][0]:
					value=value[0]+value[1]
				dict6[key]=value

#	dict7={'actual timestamp:':list1,
#	'flies on trap over time:':list2,
#	'flies in trap over time:':list3,
#	'not flies over time:':list4,
#	'seconds since release:':list5}


#	list1=dict5['actual timestamp:']
#	list2=dict5['flies on trap over time:']
#	list3=dict5['flies in trap over time:']
#	list4=dict5['not flies over time:']
#	list5=dict5['seconds since release:']
#	list6=[]
#	for i in list1[0]:
#		for j in list1[1]:
#			if j==i:
#				list6.append(list1[0].index(i))
#	start=list6[0]
#	end=list6.pop()
#	del list1[0][start:end+1]
#	del list2[0][start:end+1]
#	del list3[0][start:end+1]
#	del list4[0][start:end+1]
#	del list5[0][start:end+1]
#	if list1[0][0]>list1[1][0]:
#		list1=list1[1]+list1[0]
#		list2=list2[1]+list2[0]
#		list3=list3[1]+list3[0]
#		list4=list4[1]+list4[0]
#		list5=list5[1]+list5[0]
#	elif list1[0][0]<list1[1][0]:
#		list1=list1[0]+list1[1]
#		list2=list2[0]+list2[1]
#		list3=list3[0]+list3[1]
#		list4=list4[0]+list4[1]
#		list5=list5[0]+list5[1]

#	dict6={'actual timestamp:':list1,
#	'flies on trap over time:':list2,
#	'flies in trap over time:':list3,
#	'not flies over time:':list4,
#	'seconds since release:':list5
#	}

	return dict6


trap=input("Enter a trap letter you'd like to make a mask: ")

directory='/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap

with open(directory+'/trap_exp3_1_94313_95300.json') as f:
	data1 = json.load(f)
f.close()
dataa=remove_trapname(data1,'trap_'+trap)


with open(directory+'/trap_exp3_1_95232_95630.json') as f:
	data2 = json.load(f)
f.close()
datab=remove_trapname(data2,'trap_'+trap)


with open(directory+'/trap_exp3_1_95302_100500.json') as f:
	data3 = json.load(f)
f.close()
datac=remove_trapname(data3,'trap_'+trap)


with open(directory+'/trap_exp3_1_100101_100959.json') as f:
	data4 = json.load(f)
f.close()
datad=remove_trapname(data4,'trap_'+trap)


with open(directory+'/trap_exp3_1_101001_101059.json') as f:
	data5 = json.load(f)
f.close()
datae=remove_trapname(data5,'trap_'+trap)


with open(directory+'/trap_exp3_1_101101_102000.json') as f:
	data6 = json.load(f)
f.close()
dataf=remove_trapname(data6,'trap_'+trap)


with open(directory+'/trap_exp3_1_102002_102641.json') as f:
	data7 = json.load(f)
f.close()
datag=remove_trapname(data7,'trap_'+trap)


#master_dict=mergeDict(data3,mergeDict(data2,mergeDict(data,data1)))



pdb.set_trace()

print(data)