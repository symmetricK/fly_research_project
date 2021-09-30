#### Date: 09/30/2021
#### Author: Kei Horikawa
#### File name: Documentaton.md


Here, I note how to deal with some python scripts to analyze frames from our experiments. 
------

### This is Directory & File Structures

```bash
field_data_and_analysis_scripts
├── 2021lab
│   ├── trap_G_videos
│   ├── trap_dummy_videos
│   ├── trapcam_timelapse
│       ├── trap_exp3_1
│           ├── mask.jpg
│           ├── tl_0009_0001_20210812_094213.jpg
│           ├── tl_0009_0001_20210812_094215.jpg
│           ├── ...
│       ├── trap_exp3_2
│       ├── trap_exp4_1
│       ├── ...
│   ├── arrival_dynamic_figs
│   ├── all_traps_plots_figures
│       ├── trap_exp3_1_plots.jpg
│       ├── trap_exp3_2_plots.jpg
│       ├── trap_exp4_1_plots.jpg
│       ├── ...
│   ├── all_traps_final_analysis_json_files
│       ├── trap_exp3_1
│           ├── master_trap_exp3_1.json
│           ├── trap_exp3_1_094313_094959.json
│           ├── trap_exp3_1_095001_095959.json
│           ├── ...
│       ├── trap_exp3_2
│       ├── trap_exp4_1
│       ├── ...
│   ├── all_traps_analyzed_videos
│       ├── trap_exp3_1_videos
│           ├── 1632512844_mahal10_trainnum29
│               ├── annotated_frames
│                   ├── 1120210812095101.jpg
│                   ├── 1120210812095103.jpg
│                   ├── ...
│                   ├── 2220210812095101.jpg
│                   ├── 2220210812095103.jpg
│                   ├── ...
│                   ├── 3320210812095101.jpg
│                   ├── 3320210812095103.jpg
│                   ├── ...
│                   ├── 4420210812095101.jpg
│                   ├── 4420210812095103.jpg
│                   ├── ...
│                   ├── 5520210812095101.jpg
│                   ├── 5520210812095103.jpg
│                   ├── ...
│               ├── annotated_frames_plus_graphs
│           ├── 1632513198_mahal10_trainnum29
│           ├── 1632513531_mahal10_trainnum29
│           ├── ...
│       ├── trap_exp3_2_videos
│       ├── trap_exp4_1_videos
│       ├── ...
│   ├── all_contrast_metrics
│   ├── trap_layout_parameters.json
│   ├── field_parameters.json
│   ├── all_traps_gaussian_analysis_params.json
│   ├── all_traps_final_analysis_output.json
│   ├── all_flies_data.json
├── image_samples
├── __pycache__
├── Documentation.md
├── How_to_analyze.md
├── make_contrast_area_plot.py
├── make_plot_from_final_trap_data.py
├── making_mask.py
├── making_master_json.py
├── README.md
├── run_trapcam_analysis.py
├── trapcam_analysis.py
```
### How to use python scripts and json files 
1. Save a video file into "trapcam_timelapse" as "trap_$$$" (e.g. trap_exp3_1) 
2. Create "mask.jpg" by runnnig making_mask.py
  - Enter an experiment directory you would like to make a mask (e.g. exp3_1)
  - Enter the region of mask you want to focus on (e.g. x0:350, x1:-350, y0:100, y1:-10)
  - You may need to try this step a couple of times to set an appropriate mask region 
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/run_making_mask.png)
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/Inkedtl_0009_0272_20210812_095117%5B6761%5D_LI.jpg)
3. Add and adjust parameters on some json files
  - "field_parameters.json"
    - Change "time_of_fly_release" parameter to the time you actually released during the experiment (e.g. "09:50:00")
    - Add trap name which you would like to analyze into "trap counts" parameter (e.g. "trap counts":{"trap_exp3_1":777})
      - You can set any number of trap counts @@@
                                                          
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/release_time.png)
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/trap_counts.png)

  - "all_traps_gaussian_analysis_params.json"
    - Add trap name and parameters you wouid like to analyze
    - For now, to analyze trap data, you can just modify 2 parameters
      - "camera time advanced by __ sec":
        - At "time_of_fly_release:09:50:00", if you set 0, you will get data from "09:50:00"
        - At "time_of_fly_release:09:50:00", if you set -600, you will get data from "09:40:00"
        - At "time_of_fly_release:09:50:00", if you set 1200, you will get data from "10:10:00"
        - Running "run_trapcam_analysis.py" with changing this parameter, you will get different time frame data 
      - "analyze_how_many_minutes_post_release":
        - If you set 10, you will get 10 minutes data
 ![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/param.png)
 
4. Run "run_trapcam_analysis.py"
  - Enter a trap letter to analyze (e.g. exp3_1)

![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/run_trapcam.png)
  - After running "run_trapcam_analysis.py", you will get analyzed video data in "all_traps_analyzed_videos" directory and a subdivided json file in "all_traps_final_analysis_json_files" directory
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/before_master.png)
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/v.png)
  - Repeat step 3 (change parameters) and this step to analyze the whole trap data
5. Make master json file from subdivided json files
  - After step 4, you can see some subdivided json files in "all_traps_final_analysis_json_files" directory
  - By running "making_master_json.py" (e.g. exp3_1), you will get a master json file which has the whole trap data in "all_traps_final_analysis_json_files" directory

![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/running_master.png)
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/after_master.png)

6. Create a plot corresponding to the trap you want to alalyze
  - Run "make_plot_from_final_trap_data.py"
    - Enter a trap letter you want to analyze (e.g. exp3_1)
    - Enter released time (same as "time_of_fly_release" parameter) (e.g. 095000)
    - Enter if you want to cut last three minutes data (y or n) (e.g. y)
    - After running "make_plot_from_final_trap_data.py", you can see which frame(time) has the most flies 
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/after_running_make_a_plot.png)
    - And you can get the plot figure which you wanted to see in "all_traps_plots_figures" directory
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/plot_sample.png)

### After running python scripts 
- You can find results of analyzed video data in "all_traps_analyzed_videos" directory
- You can find the plot figure in "all_traps_plots_figures" directory
- You can find a master json fle as the whole trap data in "all_traps_final_analysis_json_files" directory
##### "all_traps_analyzed_videos" directory
all_traps_analyzed_videos──trap_exp3_1_videos──1632512844_mahal10_trainnum29──annotated_frames
