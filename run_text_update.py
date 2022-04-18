from datetime import datetime
import time
import random

n=datetime.now()
c_time=n.strftime("%H:%M:%S")
dst="/home/flyranch/field_data_and_analysis_scripts/2021lab/others/"+c_time+".txt"
count=1


while True:
	try:
		file1=open(dst, "a")
		now=datetime.now()
		current_time=now.strftime("%H:%M:%S")
		num1=random.uniform(0.7,1.3)
		r_num1=round(num1,6)
		num2=random.uniform(0.7,1.3)
		r_num2=round(num2,6)
		file1.write(current_time+"\t"+str(count)+"\t"+str(r_num1)+"\t"+str(r_num2)+"\n")
		print("Current Time =", current_time)
		file1.close()
		count+=1
	except KeyboardInterrupt:
		pass
	time.sleep(1) #wait for 1 sec


