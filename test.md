# run_trapcam_analysis.py
- to avoid inputting many times while updating files, modified some statements
- these have to be fixed when we try actual experiment

# trapcam_analysis.py
- Based on Kate's code, adjusted the code for our experiment
- to debug, used pdb.set_trace()
## def __init__(self, directory,trap='trap_A',calculate_threshold=False,calculate_final=True):
- added self.USE_FULL_MASK=True
	- test
		- test

## def load_color_image(self,filename):
- added img=img[:,400:2350] # to focus on a specific area
	- might be needed to adjust for our experiment

## def load_mask(self, square_mask_path):
- test

## def show_image_with_circles_drawn_around_putative_flies(self, color_image, flies_on_trap, flies_in_trap, not_flies):
- to get more specific information from output images, created other 3 functions
	- def show_fgmask_with_marks_drawn_around_in_trap_on_trap_flies(self,fg_mask,all_flies):
	- def show_image_with_marks_drawn_around_in_trap_on_trap_flies(self,color_image,all_flies):
	- def show_image_with_circles_drawn_around_all_flies(self,color_image, all_flies, not_flies):
		- cv2.circle(fg_mask, (fly['x'], fly['y']), 50, [255,255,255], 5)
			- to draw circle on the image
		- cv2.rectangle(fg_mask, (fly['x']-50, fly['y']+50), (fly['x']+50, fly['y']-50), [255,255,255], 5)
			- to draw rectangle on the image
		- cv2.putText(fg_mask,"on trap(circle): "+str(on_trap_count),(150,1740),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)
			- to write text on the image
			- font can be changed
		- color info might be modified for our experiment 
		- by using for loop and if conditions(fly['type']), actions are decided
		- cv2.drawMarker(color_image, (fly['x'], fly['y']),[127,127,127],cv2.MARKER_DIAMOND, 125,6)
			- to draw diamond on the image
			- triandle, star, cross, etc. can be drawn 
		- text locations might be changed for our experiment

### Test
- cv2.bitwise_and(img1, img2, mask=mask)
	- imgs has to be the same size
	- mask decides the region which we want to extract from imgs







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
- reading json file (In this case, all_traps_final_analysis_output.json) 
	- f=open(source)
	- data=json.load(f)
	- some code(In this case, make three lists)
	- f.close()
- makeing list
	- difine function to make accumulation list
	- apply the function to the three lists
- creating subplots
	- fig, (ax1, ax2) = plt.subplots(2, 1,figsize=(15,15))
	- plt.savefig(direction)

### Here is output

See (flies_time.jpg)
![flies_time.jpg](/image_samples/flies_time.jpg)<br>