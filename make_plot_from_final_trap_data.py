import json
import matplotlib.pyplot as plt
import numpy as np
import pdb

f=open('/home/flyranch/field_data_and_analysis_scripts/2017_10_26/all_traps_final_analysis_output.json')
data=json.load(f)

on_trap_list=[]
in_trap_list=[]
sec_since_release_list=[]


#ask user input

for i in data['trap_dummy']:
	for k in data['trap_dummy'][i]:
		if i=="flies on trap over time:":
			on_trap_list.append(k)
		elif i=="flies in trap over time:":
			in_trap_list.append(k)
		elif i=="seconds since release:":
			sec_since_release_list.append(k)

f.close()

on_acc_list=[]
for i in np.arange(on_trap_list):


x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('A tale of 2 subplots')

ax1.plot(sec_since_release_list, on_trap_list, 'o-')
ax1.plot(sec_since_release_list, in_trap_list, 'o-')
ax1.set_ylabel('Damped oscillation')

ax2.plot(sec_since_release_list, on_trap_list, '.-')
ax2.set_xlabel('time (s)')
ax2.set_ylabel('Undamped')
pdb.set_trace()


