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

1. Save a video file into "trapcam_timelapse" as "trap_$$$" (e.g. trap_exp3_1) 
2. Create "mask.jpg" by runnnig making_mask.py
  - Enter an experiment directory you would like to make a mask (e.g. exp3_1)
  - Enter the region of mask you want to focus on (e.g. x0:350, x1:-350, y0:100, y1:-10)
![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/run_making_mask.png)
3. Add and adjust parameters on some json files
  - "field_parameters.json"
    - change "time_of_fly_release" parameter to the time you actually released during the experiment (e.g. "09:50:00")
    ![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/release_time.png)
    - add trap name which you would like to analyze into "trap counts" parameter (e.g. "trap counts":{"trap_exp3_1":777})
      - you can set any number of trap counts @@@
    ![alt text](https://raw.githubusercontent.com/symmetricK/fly_research_project/master/image_samples/trap_counts.png)
    
