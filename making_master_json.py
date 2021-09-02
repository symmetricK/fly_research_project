import json
import matplotlib.pyplot as plt
import numpy as np
import pdb

def mergeDict(dict1, dict2,trap_key):

    ''' Merge dictionaries and keep values of common keys in list'''
    dict3={}
    dict3[trap_key] = {**dict1[trap_key], **dict2[trap_key]}
    for key, value in dict3[trap_key].items():
        if key in dict1[trap_key] and key in dict2[trap_key]:
               dict3[trap_key][key] = [value , dict1[trap_key][key]]
    return dict3


trap=input("Enter a trap letter you'd like to make a mask: ")

directory='/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap

with open(directory+'/trap_exp3_1_94313_95300.json') as f:
	data = json.load(f)

f.close()

with open(directory+'/trap_exp3_1_95232_95630.json') as f:
	data1 = json.load(f)

f.close()

with open(directory+'/trap_exp3_1_95400_100300.json') as f:
	data2 = json.load(f)

f.close()

with open(directory+'/trap_exp3_1_95302_100500.json') as f:
	data3 = json.load(f)

f.close()

master_dict=(data,data1,'trap_exp3_1')




pdb.set_trace()

print(data)