#### Date: 08/16/2022
#### Author: Kei Horikawa
#### File name: Documentaton.md

Here, I note how to deal with some python scripts to analyze frames from our experiment. 

You can go step by step

###  Step 1. copy raw data from external drive into "/home/flyranch/field_data_and_analysis_scripts/2021lab/" directory
	Just in case, keep raw data!

*Raw data were copied from external drive into "/home/flyranch/field_data_and_analysis_scripts/2021lab/" directory

### Step 2. copy raw data into trapcam_timelapse directory
Run 'python3 copy_raw_data.py'

Enetr release date (e.g. 20220317 (yyyymmdd)), then, automatically subdirectory would be created in trapcam_timelapse directory
	To complete, it takes a while

*Raw data were copied from Field_Trap_Exps directory into trapcam_directory
*At the same time, anemometer (wind) data text file was renamed and copied into "/home/flyranch/field_data_and_analysis_scripts/2021lab/wind_data_files"


### Step 3. rename image files
Run 'python3 file_rename.py'
Enter experiment date (e.g. 20220317 (yyyymmdd))
Enter "y" or "n"
	If you choose "y", the even-numbered image files in each Pi cam file will be removed

*Each image file name and subdirectory name in trapcam_timelapse directory were changed

### Step 4. create mask image in Pi cam image directory (e.g. trap_Pi6_20220725090000)
Run 'python3 create_mask.py'
Enter a trap name which you'd like to make a mask (e.g. Pi1_20220804101000)
Enter release date (e.g. 20220804 (yyyymmdd))

A test image should be pop up
To make a mask image, you need to decide 4 points for vertex on the image
To save 1 vertex x, y position, double click on the image
Now, you can see blue circle on the image
To store the vertex data, press "a" (keyboard)
To save other 3 vertex data,  do double click on the image and press "a" three times
If you are OK with these 4 vertex for a mask image, press "l"
And, press "y" on the terminal

*mask_check.jpg and mask.jpg were created in trapcam_timelapse directory
*If the mask image is not good, you should try this step again
*While running 'create_mask.py', you can quit by Ctrl+C on the terminal


### Step 5. add trap data to json files
Add information about the traps you want to analyze into "all_traps_gaussian_analysis_params.json" as well as exisiting data

Add information about the traps you want to analyze into "field_parameters.json" as well as exisiting data
Add release time (e.g. 10:55:42 (hh:mm:ss)) into "field_parameters.json"

*These json files are located in "2021lab" directory

### Step 6. do analysis 
Run 'run_trapcam_analysis.py'
Enter a trap name to analyze (e.g. 2022_03_17_WT)
Enter experiment date (e.g. 20220725 (yyyymmdd))
	To complete, it takes a while
*Annotated_frames were created in all_traps_analyzed_videos directory


### Step 7. make master json file
Run 'python3 make_master_json.py'
Enter a trap name which you'd like to make a master json file (e.g. Pi1_20220804101000)
Enter release date (e.g. 20220725 (yyyymmdd))

* master json file was created in all_traps_final_analysis_json_files directory

### Step 8. create plots for one trap
Run 'python3 make_plot_for_one_trap.py'
Enter a trap name which you'd like to create plots (e.g. 2021_10_30_C)
Enter experiment date (e.g. 20220725 (yyyymmdd))
Enter release time (e.g. 105542 (hhmmss)) @ See release note

 * Plots for one trap related to on-trap flies and in-trap flies per frame were created in 'analyzed plot figures directory' 
 * You can see the specific frame info. on the terminal, so you should note them. 
 	(e.g. frame 105604 has the first on trap fly: travel time is 22 sec
	      frame 105854 has the most flies on trap: 30
	      frame 111833 has the most flies in trap: 17)
 * Possibly, these specific frame info. were incorrect. You can double-check analyzed video images.
 
### Step 9. create plots for all traps
Run 'python3 make_plot_for_all.py'
Enter experiment date (e.g. 20220725 (yyyymmdd))
Enter release time (e.g. 105542 (hhmmss))
Enter a trap number located in upwind (e.g. 4) 
Enter another trap number located in upwind (e.g. 5) 

* Plot for all 8 traps related to on trap flies was created
* assumed 8 traps were set in a clockwise direction
 
### Step 10. create wind data plot
Run 'python3 make_wind_data_plot.py'
Enter release date (e.g. 2022_08_04 (YYYY_MM_DD))
Enter release time (e.g. 1055 (hhmm)) @ "seconds" are not required

* Plot for wind data from anemometer was created in wind_plot_figures directory
* On the plot, vertical blue dot line shows release time, and black bar shows wind direction at that time
 
 
 
 
