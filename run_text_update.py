from datetime import datetime
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import pdb

now=datetime.now()
c_time=now.strftime("%Y%m%d%H%M%S")

dst="/home/flyranch/field_data_and_analysis_scripts/2021lab/others/"+"fly4_"+c_time[:8]+"_"+c_time[8:]+".txt"
count=1
MAX_VALUE=4060
#dst_plot="/home/flyranch/field_data_and_analysis_scripts/2021lab/others/"+c_time+".png"
#x_list=[]
#y_list=[]


#pdb.set_trace()
while True:
	try:
		file1=open(dst, "a")
		now=datetime.now()
		current_time=now.strftime("%H%M%S")
		f_num=format(count,'.6f')
		num1=random.uniform(0.7,1.3)
#		r_num1=round(num1,6)
		r_num1=format(round(num1,6),'.6f')
		num2=random.uniform(0.7,1.3)
#		r_num2=round(num2,6)
		r_num2=format(round(num2,6),'.6f')
		
		fic_position=np.random.choice(np.arange(1,MAX_VALUE))

		file1.write(f_num+"\t"+str(fic_position)+"\t"+str(r_num1)+"\t"+str(r_num2)+"\n")
		
		print("Current Time =", current_time)
		file1.close()
		count+=1
#		plt.plot(current_time,r_num1)
#		plt.savefig(dst_plot)
	except KeyboardInterrupt:
		pass
#	time.sleep(1) #wait for 1 sec
#	time.sleep(5) #wait for 5 sec
	time.sleep(0.01) #wait for 0.01 sec
