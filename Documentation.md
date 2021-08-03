## I am going to make a list
- Text here
- Text here

More text
- 
-

See (before_change.jpg)<br>
![before_change.jpg](/image_samples/before_change.jpg)<br>


See (all_detections.jpg)<br>
![all_detections.jpg](/image_samples/all_detections.jpg)<br>
See (fgmask_in_on_detections.jpg)
![fgmask_in_on_detections.jpg](/image_samples/fgmask_in_on_detections.jpg)<br>
See (in_on_detections.jpg)
![in_on_detections.jpg](/image_samples/in_on_detections.jpg)<br>
See (original_frame.jpg)
![original_frame.jpg](/image_samples/original_frame.jpg)<br>
See (4figures.jpg)
![4figures.jpg](/image_samples/4figures.jpg)<br>






# make_plot_from_final_trap_data.py
- reading json file
	- f=open(source)
	- data=json.load(f)
	- some code(In this case, make three lists)
	- f.close()
- makeing list
- creating subplots

### reading json file



### making list
- difine function to make accumulation list
- apply the function to the three lists

### creating subplots
- fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(15,15))
- plt.savefig(direction)

Here is output

See (flies_time_plot.jpg)
![flies_time_plot.jpg](/image_samples/flies_time_plot.jpg)<br>