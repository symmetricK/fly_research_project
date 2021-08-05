import json
import matplotlib.pyplot as plt
import numpy as np
import pdb

f=open('/home/flyranch/field_data_and_analysis_scripts/2017_10_26/all_flies_data.json')
data=json.load(f)

data_list=[]
contour_area_list=[]
contrast_list=[]


#ask user input
trap=input("Enter a trap letter to analyze: ")

#for i in data['trap_'+trap]:
#	data_list.append(i)

pdb.set_trace()


#	for j in data['trap_'+trap][i]:
#		pdb.set_trace()
#		for k in data['trap_'+trap][i][j]:
#			if j=="area":
#				contour_area_list.append(k)
#			elif j=="contrast metric":
#				contrast_list.append(k)


pdb.set_trace()


f.close()

