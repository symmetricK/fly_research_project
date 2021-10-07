import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import os
import glob
import sys

def remove_trapname(dict1,key):
	'''remove trap_name to merge two dicts'''
	dict2=dict1[key]
	return dict2


def merge_dict(dict3,dict4):
	''' Merge dictionaries and keep values of common keys in list
		Remove duplicate values
		'''

	dict5 = {**dict3, **dict4}

	for key, value in dict5.items():
		if key in dict3 and key in dict4:
			dict5[key] = [value , dict3[key]]


	duplicate_index_list=[]
	for key, value in dict5.items():
		if key=='actual timestamp:':
			#try:
			for i in value[0]:
				for j in value[1]:
					if j==i:
						duplicate_index_list.append(value[0].index(i))
#			except:
#				pdb.set_trace()

	if len(duplicate_index_list) > 0:
		start=duplicate_index_list[0]
		end=duplicate_index_list[-1]
		for value in dict5.values():
			del value[0][start:end+1]

	dict6={}
	
#	try:
	for key,value in dict5.items():

		if (len(dict5['actual timestamp:'][0])==0):
			value=value[1]
		elif (len(dict5['actual timestamp:'][1])==0):
			value=value[0]
		else:
			if dict5['actual timestamp:'][0][0]>dict5['actual timestamp:'][1][0]:
				value=value[1]+value[0]
			elif dict5['actual timestamp:'][0][0]<dict5['actual timestamp:'][1][0]:
				value=value[0]+value[1]
		dict6[key]=value
	dict5={}
	return dict6


trap=input("Enter a trap letter you'd like to make a mask: ")

directory='/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap


all_json_dicts=[]
#for json_file in os.listdir(directory):
#    full_filename="%s/%s" % (directory,json_file)
#    with open(full_filename,'r') as f:
#        dic=json.load(f)
#        all_json_dicts.append(dic)

#f.close()


file_list=sorted(glob.glob(directory+('/*json')))

for file_name in file_list:
    with open(file_name,'r') as f:
        dic=json.load(f)
        all_json_dicts.append(dic)

f.close()



all_json_dicts_list=[]
for json_dict in all_json_dicts:
	json_dict_removed=remove_trapname(json_dict,'trap_'+trap)
	all_json_dicts_list.append(json_dict_removed)


m_j_list=[]
initial_json_dict={}
temp_json_dict={}
merged_json={}
count=0
for file in all_json_dicts_list:
	if count==0:
		initial_json_dict=file
	elif count==1:
		temp_json_dict=file
		merged_json=merge_dict(initial_json_dict,temp_json_dict)
	else:
		temp_json_dict=file
		merged_json=merge_dict(merged_json,temp_json_dict)
	count+=1
	m_j_list.append(merged_json)

print('creating master json file...')

master_json={'trap_'+trap:merged_json}

json_filename='/master_trap_'+trap+'.json'

json_path=directory+json_filename
if not os.path.exists(json_path):
    with open(json_path,'w') as json_file:
        json.dump(master_json,json_file,indent=1)
else:
	y_n=input("master json file has alredy exists. Do you want to overwrite it? (y or n): ")
	if y_n=="y":
		print('master json file was overwritten')
		with open(json_path,'w') as json_file:
			json.dump(master_json,json_file,indent=1)
	if y_n=="n":
		sys.exit()


