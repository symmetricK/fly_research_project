#! /usr/bin/python

from __future__ import print_function
import cv2 # opencv
import numpy as np
import os, sys
import matplotlib.pyplot as plt
import time
import json
from pylab import *
from scipy.optimize import curve_fit
# from scipy.stats import gamma
#from pympler.tracker import SummaryTracker
import subprocess
import pdb

#tracker = SummaryTracker()

class TrapcamAnalyzer:
    def __init__(self, directory, trap='trap_A', 
    	calculate_threshold=False, calculate_final=True):  # <---- instances of this class will specify the directory, most likely using directory = sys.argv[1]
        self.directory = directory
        self.USE_FULL_MASK=True
        self.trap = trap
        #print(threshold)
        #self.calculate_threshold=calculate_threshold
        self.calculate_threshold = False
        self.calculate_final = calculate_final
        # initialize expectations here; can update the value of each self.variable later
        with open(self.directory+'/all_traps_gaussian_analysis_params.json') as f:
            self.analysis_parameters_json = json.load(f)
        with open(self.directory+'/field_parameters.json') as f:
            self.field_parameters = json.load(f)

        self.train_num                    = self.analysis_parameters_json[trap]['analysis parameters']["number of frames for bg model training"]
        self.mahalanobis_squared_thresh   = self.analysis_parameters_json[trap]['analysis parameters']['mahalanobis squared threshold']
        self.buffer_btw_training_and_test = self.analysis_parameters_json[trap]['analysis parameters']['frames between training and test'] # if too high, shadows get bad
        self.minimum_in_trap_contour_size = self.analysis_parameters_json[trap]['analysis parameters']['minimum_in_trap_contour_size']
        self.maximum_in_trap_contour_size = self.analysis_parameters_json[trap]['analysis parameters']['maximum_in_trap_contour_size']
        self.minimum_on_trap_contour_size = self.analysis_parameters_json[trap]['analysis parameters']['minimum_on_trap_contour_size']
        self.maximum_on_trap_contour_size = self.analysis_parameters_json[trap]['analysis parameters']['maximum_on_trap_contour_size']
        self.min_prior_to_r               = self.analysis_parameters_json[trap]['analysis parameters']["analyze_how_many_minutes_prior_to_release"]
        self.min_post_r                   = self.analysis_parameters_json[trap]['analysis parameters']["analyze_how_many_minutes_post_release"]
        self.release_time                 = self.field_parameters["time_of_fly_release"]
        self.camera_offset                = self.analysis_parameters_json[trap]['analysis parameters']["camera time advanced by __ sec"]
        self.trimodal_expected            = tuple(self.analysis_parameters_json[trap]['analysis parameters']['trimodal expected'])
        self.save_video                   = self.analysis_parameters_json[trap]['analysis parameters']["save frames as video"]

        #things that aren't yet in the analysis parameter files because I'm still finagling them:
        self.minimum_contrast_metric = 1
        self.linear_relationship_slope = -20.0
        self.linear_relationship_offset = 600.0
        ################################################################################################

        if self.calculate_final == True:
            try:
                self.ontrap_intrap_threshold = self.analysis_parameters_json[trap]['analysis parameters']["fixed in-trap on-trap threshold"]
            except:
###                use_provisional_value =input('Looks like you have not yet fixed the in-trap/on-trap threshold; use provisional threshold? (y/n)')
                use_provisional_value='y'
                if use_provisional_value:
                    self.ontrap_intrap_threshold = self.analysis_parameters_json[trap]['analysis parameters']["threshold to differentiate in- and on- trap"]
                else:
                    print ('OK, skipping '+ self.trap+' for now')
                    print ('')
                    ### NEED TO FIND A WAY TO HANDLE THIS CASE

        else:
            self.ontrap_intrap_threshold = self.analysis_parameters_json[trap]['analysis parameters']["threshold to differentiate in- and on- trap"]

        plt.rcParams.update({'font.size': 14}) # <--- there is probably a better place to specify this so it's more flexible, but this'll work for now


    def get_filenames(self, path, contains, does_not_contain=['~', '.pyc']):
        cmd = 'ls ' + '"' + path + '"'
        ls = os.popen(cmd).read()
        all_filelist = ls.split('\n')
        try:
            all_filelist.remove('')
        except:
            pass
        filelist = ['']*(len(all_filelist))
        filename_count = 0
        for i, filename in enumerate(all_filelist):
            if contains in filename:
                fileok = True
                for nc in does_not_contain:
                    if nc in filename:
                        fileok = False
                if fileok:
                    #filelist.append( os.path.join(path, filename) )
                    filelist[filename_count] = str(os.path.join(path,filename))
                    filename_count +=1
        filelist_trimmed = filelist[0:filename_count-1]
        return filelist_trimmed

    def load_color_image(self, filename):
        #header = "\xff\xd8"
        #tail = "\xff\xd9"
       
        #with open(filename, "rb") as image:
         #   data = image.read()
          #  try:
           #     start = data.index(header)
            #    end = data.index(tail, start) + 2
            #except ValueError:
             #   print ("Can't find JPEG data!")
              #  return None
        img = cv2.imread(filename)
        return img

    def load_mask(self, square_mask_path):
        print (square_mask_path)
        mask = cv2.imread(square_mask_path)
        gray_mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        rescaled_mask = np.int8(floor(gray_mask/255)) #rescales mask to be 0s and 1s     
        return rescaled_mask

    def fit_ellipse_to_contour(self, contour):
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00']) # centroid, x
            cy = int(M['m01']/M['m00']) # centroid, y
            area = cv2.contourArea(contour)
            if len(contour)>5:
                ellipse = cv2.fitEllipse(contour)
                (x,y), (a,b), angle = ellipse
                a /= 2.
                b /= 2.
                eccentricity = np.min((a,b)) / np.max((a,b))
                eccentricity = round(eccentricity, 3)
                return cx, cy, area, eccentricity
            else:
                return cx, cy, area, 'None'
        else:
            return None
        #return cx, cy, area

    def smooth_image(self, thresh_img):
        morph_ellipse_size = (3,3)#(3,3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_ellipse_size)
        morph_open_iteration_number = 2
        morph_close_iteration_number = 8
        thresh_img_smooth = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations = morph_open_iteration_number)
        thresh_img_smooth = cv2.morphologyEx(thresh_img_smooth, cv2.MORPH_CLOSE, kernel, iterations = morph_close_iteration_number)
        # thresh_img_smooth = cv2.dilate(thresh_img_smooth, kernel, iterations=10) # make the contour bigger to join neighbors
        # thresh_img_smooth = cv2.erode(thresh_img_smooth, kernel, iterations=10) # make contour smaller again
        return thresh_img_smooth, morph_open_iteration_number, morph_ellipse_size

    def get_time_since_release_from_filename (self, name = ''):
        frame_time_string = name.split('.')[-2].split('_')[-1]
        frame_hour = int(frame_time_string[0:2])
        frame_min = int(frame_time_string[2:4])
        frame_sec = int(frame_time_string[4:6])
        frame_seconds_timestamp = (frame_hour)*3600 + (frame_min)*60 + (frame_sec)
        frame_seconds = frame_seconds_timestamp - self.camera_offset
        release_time_seconds = int(self.release_time.split(':')[0])*3600 +int(self.release_time.split(':')[1])*60 + int(self.release_time.split(':')[2])
        time_elapsed = frame_seconds - release_time_seconds
        return time_elapsed

    def show_image_with_circles_drawn_around_putative_flies(self, color_image, flies_on_trap, flies_in_trap, not_flies):
        font = cv2.FONT_HERSHEY_SIMPLEX

        for fly in flies_on_trap:
            if fly['perimeter contrast boolean']:
                color = [0,0,0]
            else:
                color = [0,0,153]
            cv2.circle(color_image, (fly['x'], fly['y']), 50, color, 5)
            cv2.putText(color_image, str(fly['area']),(fly['x']+50, fly['y']-50), font, 1, color,2, cv2.LINE_AA)
            cv2.putText(color_image, str(int(fly['contrast metric'])),(fly['x']+50, fly['y']+50), font, 1, color,2, cv2.LINE_AA)
            #cv2.putText(color_image, str(fly['perimeter contrast boolean']),(fly['x']+50, fly['y']+50), font, 1, (0,0,0),2, cv2.LINE_AA)

        for fly in flies_in_trap:
            if fly['perimeter contrast boolean']:
                color = [153,0,153]
            else:
                color = [0,0,153]
            cv2.circle(color_image, (fly['x'], fly['y']), 50, color, 5)
            cv2.putText(color_image, str(fly['area']),(fly['x']+50, fly['y']-50), font, 1, color,2, cv2.LINE_AA)
            cv2.putText(color_image, str(int(fly['contrast metric'])),(fly['x']+50, fly['y']+50), font, 1, color,2, cv2.LINE_AA)
            #cv2.putText(color_image, str(fly['perimeter contrast boolean']),(fly['x']+50, fly['y']+50), font, 1, [153,0,153],2, cv2.LINE_AA)

        for not_fly in not_flies:
            cv2.circle(color_image, (not_fly['x'], not_fly['y']), 50, [178,255,102], 5)
            cv2.putText(color_image, str(not_fly['area']),(not_fly['x']+50, not_fly['y']-50), font, 1, [178,255,102],2, cv2.LINE_AA)

    def plot_2d_scatter(self,
                            all_contrast_metrics,
                            all_fly_contour_areas,
                            current_frame_contrast_metrics,
                            current_frame_fly_contour_areas,
                            ax_handle):

        plt.scatter(all_contrast_metrics, all_fly_contour_areas, color = 'black', s =1)
        plt.scatter(x = current_frame_contrast_metrics, y = current_frame_fly_contour_areas, color = [1.0,0.35,0], s = 40, edgecolors = ['black'])
        # plt.axhline(y = self.minimum_on_trap_contour_size, color = 'black', lw =2, xmin=(self.ontrap_intrap_threshold - 5.)/(45-5.) , xmax =1.0)
        # plt.axhline(y = self.maximum_on_trap_contour_size, color = 'black', lw =2, xmin=(self.ontrap_intrap_threshold - 5.)/(45-5.) , xmax =1.0)
        # plt.axhline(y = self.minimum_in_trap_contour_size, color = [0.6,0,0.6], lw =2, xmin=0, xmax =(self.ontrap_intrap_threshold - 5.)/(45-5.))
        # plt.axhline(y = self.maximum_in_trap_contour_size, color = [0.6,0,0.6], lw =2,xmin= 0, xmax =(self.ontrap_intrap_threshold - 5.)/(45-5.))
        #plt.axvline(x = self.ontrap_intrap_threshold, color = 'black',lw=2)
        plt.plot(np.linspace(5,45,300), [x*self.linear_relationship_slope +self.linear_relationship_offset for x in np.linspace(5,45,300)], '--k')
        ax_handle.spines['right'].set_visible(False)
        ax_handle.spines['top'].set_visible(False)
        ax_handle.set_ylim(0,self.maximum_on_trap_contour_size*1.2)
        ax_handle.set_xlim(5,45)
        # Only show ticks on the left and bottom spines
        ax_handle.yaxis.set_ticks_position('left')
        ax_handle.xaxis.set_ticks_position('bottom')
        ax_handle.tick_params(direction='out')#, length=6, width=2, colors='r',grid_color='r', grid_alpha=0.5)

    def eliminate_foreground_pixels_brighter_than_bgimg(self, fgbg, test_image):
        fgmask_not_smoothed = fgbg.apply(test_image, None, 0)# the 0 specifies that no learning is occurring
        bgimg = fgbg.getBackgroundImage()
        gray_bgimg = cv2.cvtColor(bgimg, cv2.COLOR_RGB2GRAY)
        gray_test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)
        mask = cv2.inRange(fgmask_not_smoothed, 240, 255)
        bg_masked_by_fgmask = cv2.bitwise_and(gray_bgimg, gray_bgimg, mask=mask).astype(int16)
        test_image_masked_by_fgmask = cv2.bitwise_and(gray_test_image, gray_test_image, mask=mask).astype(int16)
        difference_img_under_mask = np.subtract(np.array(test_image_masked_by_fgmask), np.array(bg_masked_by_fgmask))
        fgmask_not_smoothed[np.where(difference_img_under_mask > 0)] = 0 # <----- for any regions in which the test image is brighter than the bgimg, mask them out
        return fgmask_not_smoothed

    #### eventually want to not use this ####
    # def report_contrast_around_contour_perimeter(self, x, y, gray_test_image,stencil, count): # stencil is 0s and 1s, dtype uint8
    #     fg_masked_by_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=stencil)
    #
    #     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    #     stencil_dilated = cv2.dilate(stencil, kernel, iterations=1)
    #     fg_masked_by_dilated_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=np.subtract(stencil_dilated, stencil))
    #     # cv2.imshow('',fg_masked_by_dilated_contour)
    #     # cv2.waitKey(1)
    #     cv2.imwrite('./examples_of_perimeter_contrast_analysis/' + "%04d.jpg" % count,fg_masked_by_dilated_contour)
    #     dilated_contour_mean = np.mean(fg_masked_by_dilated_contour) # brighter edge -> closer to zero
    #     dilated_contour_variance = np.var(fg_masked_by_dilated_contour)
    #     contour_mean = np.mean(fg_masked_by_contour) # darker interior -> closer to 255
    #     return dilated_contour_mean/contour_mean, dilated_contour_variance
    ###################################################


    def image_cropped_by_mask(self, mask):
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        return rmin, rmax, cmin, cmax

    # def examine_contrast_around_contour_perimeter(self, x, y, gray_test_image,stencil): # stencil is 0s and 1s, dtype uint8
    #     #ok, in this attempt I will be doing edge-detection within the dilated masked area, then asking if the detected edge is closed or not
    #
    #     img,contour_of_stencil,hierarchy = cv2.findContours(stencil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    #     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,21))
    #     stencil_dilated = cv2.dilate(stencil, kernel, iterations=1)
    #     fg_masked_by_dilated_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=stencil_dilated)
    #     rmin,rmax,cmin,cmax = self.image_cropped_by_mask(stencil_dilated)
    #     median = np.median(fg_masked_by_dilated_contour[rmin:rmax, cmin:cmax])
    #     edges = cv2.Canny(fg_masked_by_dilated_contour,0.2*median,0.85*median, apertureSize = 3) #was 30,90
    #     #edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 1)
    #
    #     edgesCopy = edges.copy()
    #     #fg_masked_by_dilated_contour = np.bitwise_or(fg_masked_by_dilated_contour, edgesCopy)
    #     fg_masked_by_dilated_contour = cv2.cvtColor(fg_masked_by_dilated_contour, cv2.COLOR_GRAY2BGR)
    #     #now querying whether at least one of the edges is a closed contour
    #
    #     img,contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     retval = False
    #     for component in zip(contours[2:], hierarchy[0][2:]): #skipping the first two contours because they will be the inner and outer Canny edge of the dilated stencil
    #         currentContour = component[0]
    #         currentHierarchy = component[1]
    #         if currentHierarchy[2] > 0:
    #             print ('this edge is closed (its contour has a child)')
    #             cv2.drawContours(fg_masked_by_dilated_contour, [currentContour],0,(0,0,255),1)
    #             retval = True
    #     #cv2.drawContours(fg_masked_by_dilated_contour, contour_of_stencil,0,(0,125,0),1)
    #     out = fg_masked_by_dilated_contour[y-40:y+40, x-40:x+40]
    #     cv2.imshow('', cv2.resize(out, (972,972)))
    #     wait_key_val = cv2.waitKey(0) & 0xFF
    #     if wait_key_val == ord('f'):
    #         exitloop = False
    #         return retval, exitloop
    #     if wait_key_val == ord('q'):
    #         exitloop = True
    #         return retval, exitloop

    def examine_contrast_around_contour_perimeter(self, x, y, gray_test_image,stencil,count): # stencil is 0s and 1s, dtype uint8
        contour_of_stencil,hierarchy = cv2.findContours(stencil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21,21))
        stencil_dilated = cv2.dilate(stencil, kernel, iterations=1)
        fg_masked_by_dilated_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=stencil_dilated)
        fg_masked_by_dilated_contour = cv2.cvtColor(fg_masked_by_dilated_contour, cv2.COLOR_GRAY2BGR)
        fg_masked_copy = copy(fg_masked_by_dilated_contour)
        rmin,rmax,cmin,cmax = self.image_cropped_by_mask(stencil_dilated)
        fg_cropped = fg_masked_by_dilated_contour[rmin:rmax, cmin:cmax]
        percentile25_black_excluded = np.percentile(fg_cropped[np.nonzero(fg_cropped)],25)
        fg_masked_by_dilated_contour[rmin,cmin]=255
        fg_masked_by_dilated_contour[rmax,cmin]=255
        fg_masked_by_dilated_contour[rmin,cmax]=255
        fg_masked_by_dilated_contour[rmax,cmax]=255
        ret,fg_masked_by_dilated_contour_thresh = cv2.threshold(fg_masked_by_dilated_contour,percentile25_black_excluded,255,cv2.THRESH_BINARY)

        retval = False
        black_and_white = cv2.cvtColor(fg_masked_by_dilated_contour_thresh,cv2.COLOR_BGR2GRAY)
        thresholded_masked_by_orig_contour = cv2.bitwise_and(black_and_white, black_and_white, mask=stencil)
        output_val = np.float(np.count_nonzero(thresholded_masked_by_orig_contour))/ np.float(np.count_nonzero(stencil))
        if output_val < 0.32:
            retval = True #meaning this contour is flagged as probably a fly
        else:
            retval = False

        #############comment out this block once you're done troubleshooting
        cv2.drawContours(fg_masked_by_dilated_contour_thresh, contour_of_stencil,0,(0,255,0),1)
        out = fg_masked_by_dilated_contour_thresh[y-40:y+40, x-40:x+40]
        out2 = np.concatenate((out, fg_masked_copy[y-40:y+40, x-40:x+40]), axis=1)
        try:
            cv2.imwrite('./examples_of_perimeter_contrast_analysis/' + "%04d.jpg" % count, cv2.resize(out2, (1600,800)))
        except:
            pdb.set_trace()
        
        # cv2.imshow('', cv2.resize(out2, (1600,800)))
        # wait_key_val = cv2.waitKey(0) & 0xFF
        # if wait_key_val == ord('f'):
        #     exitloop = False
        #     return retval, exitloop
        # if wait_key_val == ord('q'):
        #     exitloop = True
        #     return retval, exitloop
        #############################################################################################################

        exitloop = False
        return retval, exitloop

    def testing_step_of_backsub_MOG2(self, index, fgbg, test_image, time_since_release):

        #fgmask_notsmoothed = fgbg.apply(test_image, None, 0) # the 0 specifies that no learning is occurring   <--- this yields a 2d matrix of 0s and 255s as the foreground mask
        fgmask_notsmoothed = self.eliminate_foreground_pixels_brighter_than_bgimg(fgbg,test_image)

        fgmask1, morph_open_iteration_number, morph_ellipse_size = self.smooth_image(fgmask_notsmoothed)
        
        contours, hierarchy = cv2.findContours(fgmask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        flies_on_trap = [{} for _ in range(30000)]
        flies_in_trap = [{} for _ in range(30000)]
        not_flies     = [{} for _ in range(30000)] # this is massively preallocated but every so often a frame detects a lot of not_flies (e.g. illumination changes)
        fly_contours  = [[] for _ in range(30000)] # < -------- bummer that I need to pre-allocate this as such a chunky thing (was in range 200, moved up to 800)
        frame_contrast_metrics = np.zeros(30000)
        frame_fly_contour_areas = np.zeros(30000)
        contrast_metric_count=0
        fly_contour_area_count =0
        flies_on_trap_count=0
        flies_in_trap_count=0
        not_flies_count=0
        fly_contours_count=0
        for contour in contours:
            # if len(contour) > 5:
            x, y, area, ecc = self.fit_ellipse_to_contour(contour)
            fly = {'x': x, 'y': y, 'area': area, 'eccentricity': ecc}
            
            if area < self.maximum_on_trap_contour_size and area > self.minimum_in_trap_contour_size:
                if ecc == 'None':
                    print ('unable to fit ellipse to this contour; too small')
                else:
                    if ecc > 0.35:
                        fly_contours[fly_contours_count]=(contour)
                        fly_contours_count +=1
                    else:
                        print ('eccentricity less than 0.35')
            else:
                not_flies[not_flies_count] = fly
                not_flies_count +=1
           


        #now that we have a list of fly contours, let's see if they're inside the trap or outside it -- on the basis of contrast and area ranges
        #also, let's take this opportunity to get rid of any "flies" that are brighter than the background image. It would in theory make sense to do this earlier, but I think the mahalanobis distance might be an absolute value
        bgimg = fgbg.getBackgroundImage()
        gray_bgimg = cv2.cvtColor(bgimg, cv2.COLOR_RGB2GRAY)
        gray_test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)
        #color = 255
        color = 1
        not_flies = not_flies[0:not_flies_count]
        fly_contours = fly_contours[0:fly_contours_count]

        ########## to make a foreground- background image for troubleshooting #############################
        stencil = np.zeros(gray_bgimg.shape).astype(gray_bgimg.dtype)
        cv2.fillPoly(stencil, fly_contours, color)
        pts = np.where(stencil == 1)
        bg_masked_by_contour = cv2.bitwise_and(gray_bgimg, gray_bgimg, mask=stencil)
        fg_masked_by_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=stencil)
        difference_img_all_contours = bg_masked_by_contour - fg_masked_by_contour
        ########## to make a foreground- background image for troubleshooting #############################
        count = 1
        for fly_contour in fly_contours: #these are all the contours whose area is > min and < max contour size specified in analysis params
            stencil = np.zeros(gray_bgimg.shape).astype(gray_bgimg.dtype)
            cv2.fillPoly(stencil, [fly_contour], color) # needed to put fly_contour in a list structure, otherwise it treats each point as an individual contour
            pts = np.where(stencil == 1)
            bg_masked_by_contour = cv2.bitwise_and(gray_bgimg, gray_bgimg, mask=stencil)
            fg_masked_by_contour = cv2.bitwise_and(gray_test_image, gray_test_image, mask=stencil)
            difference_img = bg_masked_by_contour - fg_masked_by_contour
            mean_difference_in_this_contour = np.mean(bg_masked_by_contour[pts[0],pts[1]])    -    np.mean(fg_masked_by_contour[pts[0],pts[1]])
            pixel_num_in_this_contour = len(pts)
            contrast_metric = mean_difference_in_this_contour
            x, y, area, ecc = self.fit_ellipse_to_contour(fly_contour)
            #perimeter_contrast_metric, perimeter_variance = self.report_contrast_around_contour_perimeter(x, y, gray_test_image, stencil, count)
            perimeter_contrast_boolean, exitloop = self.examine_contrast_around_contour_perimeter(x, y, gray_test_image, stencil, count)
            count +=1
            if exitloop:
                break
            fly = {'x': x, 'y': y, 'area': area,'contrast metric': contrast_metric, 'perimeter contrast boolean': perimeter_contrast_boolean}

            if contrast_metric < self.minimum_contrast_metric:
                continue
            if not perimeter_contrast_boolean:
                continue

            ##################################################################
            # if contrast_metric > self.ontrap_intrap_threshold:
            #     if area > self.minimum_on_trap_contour_size: #we already know that this contour's area is less than the maximum_on_trap_contour_size, from above
            #         flies_on_trap[flies_on_trap_count]= fly
            #         flies_on_trap_count +=1
            # if contrast_metric < self.ontrap_intrap_threshold:
            #     if area < self.maximum_in_trap_contour_size: #we already know that this contour's area is more than the minimum_in_trap_contour_size, from above
            #         flies_in_trap[flies_in_trap_count]= fly
            #         flies_in_trap_count +=1
            #######################################################################

            # ###### trying out a linear relationship between contrast_metric and area as the differentiator between in_trap and on_trap flies:
            if area > self.linear_relationship_slope*contrast_metric +self.linear_relationship_offset: #if above this line, the slope and y-offset of which were empirically eyeballed based on 2019_06_11 trap_G
                if area > self.minimum_on_trap_contour_size:
                    flies_on_trap[flies_on_trap_count]= fly
                    flies_on_trap_count +=1

            if area < self.linear_relationship_slope*contrast_metric +self.linear_relationship_offset: #if below this same line, the slope and y-offset of which were empirically eyeballed based on 2019_06_11 trap_G
                if area < self.maximum_in_trap_contour_size:
                    flies_in_trap[flies_in_trap_count]= fly
                    flies_in_trap_count +=1

            frame_contrast_metrics[int(contrast_metric_count)]=contrast_metric # I use this list to see if there is sufficient bimodality in contrast metrics that the location of its local minimum could be used to automatically select a threshold for classifying in-trap vs. on-trap flies
            contrast_metric_count += 1
            frame_fly_contour_areas[int(fly_contour_area_count)]=area
            fly_contour_area_count +=1

        # now trimming trailing empty dictionaries
        flies_on_trap = flies_on_trap[0:flies_on_trap_count]
        flies_in_trap = flies_in_trap[0:flies_in_trap_count]
        ##############################################################################################
        test_image_copy = test_image.copy()
        self.show_image_with_circles_drawn_around_putative_flies(test_image_copy, flies_on_trap,flies_in_trap, not_flies)
        dict_to_add_to_all_flies_over_time = {'seconds since release':time_since_release, 'flies on trap': flies_on_trap, 'flies in trap': flies_in_trap, 'not_flies': not_flies}
        frame_contrast_metrics = frame_contrast_metrics[0:contrast_metric_count]
        frame_fly_contour_areas = frame_fly_contour_areas[0:fly_contour_area_count]
        return test_image_copy, time_since_release, dict_to_add_to_all_flies_over_time, frame_contrast_metrics, contrast_metric_count, frame_fly_contour_areas, morph_open_iteration_number, morph_ellipse_size, difference_img_all_contours #fg_masked_by_contour#difference_img #fgmask1  #fgmask_notsmoothed

    def find_contours_using_pretrained_backsub_MOG2(self,
                                                    full_image_stack,
                                                    filename_stack,
                                                    video_dir):
        fgbg = cv2.createBackgroundSubtractorMOG2(history =self.train_num, varThreshold = self.mahalanobis_squared_thresh, detectShadows = False)
        standard_out_array_length = len(full_image_stack) -self.train_num -self.buffer_btw_training_and_test
        sample_image_zero =  np.zeros_like(full_image_stack[0]) # <---- just using the first image as an "example" to be sure I preallocate the array with the right data type, dimensions etc
        # annotated_output_stack = np.stack([sample_image_zero for _ in range(standard_out_array_length)], axis = 0)
    
        time_since_release_list = np.zeros(standard_out_array_length)
        analyzed_filename_stack = ['']*(standard_out_array_length)
        all_flies_over_time = [{} for _ in range(standard_out_array_length)]  # <-----

        all_contrast_metrics = np.zeros(standard_out_array_length*2000)# <---- vastly over-allocated assuming 2000 flies per analyzed frame; will need to trim zeros using a counter of contrast metrics
        contrast_metric_count = 0
        last_frame_contrast_metric_count =0

        all_fly_contour_areas = np.zeros(standard_out_array_length*2000)
        fly_contour_area_count = 0
        last_frame_fly_contour_area_count=0

        contrast_metric_list_of_lists=[]
        fly_contour_area_list_of_lists=[]
        for index, training_image in enumerate(full_image_stack):
            fgbg.apply(training_image, None, -1) # TRAINING STEP.
            if index > self.train_num-1: # when current index is less than train_num, the model hasn't been trained on the specified number of frames. After this point, the declaration of history = train_num should make the model "forget" earlier frames so it works as a sliding window
                test_index = index+self.buffer_btw_training_and_test
                try:
                    test_image = full_image_stack[test_index]
                    test_filename = filename_stack[test_index]
                except:
                    break

                annotated_output_image, time_since_release, dict_to_add_to_all_flies_over_time, frame_contrast_metrics, frame_contrast_metric_count, frame_fly_contour_areas, morph_open_iteration_number, morph_ellipse_size, smoothed_foreground_mask  = self.testing_step_of_backsub_MOG2(index, fgbg, test_image, self.get_time_since_release_from_filename(name = test_filename))
                time_since_release_list [index -self.train_num] = time_since_release
                analyzed_filename_stack [index -self.train_num] = test_filename
                all_flies_over_time     [index -self.train_num] = dict_to_add_to_all_flies_over_time

                contrast_metric_count += frame_contrast_metric_count
                all_contrast_metrics[last_frame_contrast_metric_count:contrast_metric_count] = frame_contrast_metrics
                last_frame_contrast_metric_count = contrast_metric_count

                fly_contour_area_count += len(frame_fly_contour_areas)
                all_fly_contour_areas[last_frame_fly_contour_area_count:fly_contour_area_count] = frame_fly_contour_areas
                last_frame_fly_contour_area_count = fly_contour_area_count

                contrast_metric_list_of_lists.append(frame_contrast_metrics)
                fly_contour_area_list_of_lists.append(frame_fly_contour_areas)

                #here, save annotated output image
                #cv2.imwrite(video_dir + "%04d.jpg" % index, annotated_output_image)

                ## KH,TW NO NEED TO RESIZE 7.20.21

                #annotated_out_resized = cv2.resize(annotated_output_image, (1296,972)) #halves image dimensions just for display purposes
                #annotated_out_resized = annotated_out_resized[:,200:-240].copy()
                # smoothed_foreground_mask_resized = cv2.resize(smoothed_foreground_mask, (1296,972)) #halves image dimensions just for display purposes
                # smoothed_foreground_mask_resized = smoothed_foreground_mask_resized[:,200:-240].copy()
                # smoothed_foreground_mask_resized = cv2.cvtColor(smoothed_foreground_mask_resized,cv2.COLOR_GRAY2BGR)
                # vis = np.concatenate((annotated_out_resized, smoothed_foreground_mask_resized), axis=1)
                # cv2.imwrite(video_dir + "%04d.jpg" % index, vis)
                #cv2.imwrite(video_dir + "%04d.jpg" % index, annotated_out_resized)                
                cv2.imwrite(video_dir + "%04d.jpg" % index, annotated_output_image)

        all_contrast_metrics = all_contrast_metrics[0:contrast_metric_count-1] #trimming trailing zeros
        all_fly_contour_areas = all_fly_contour_areas[0:fly_contour_area_count-1]# trimming trailing zeros
        return all_flies_over_time, time_since_release_list, analyzed_filename_stack, all_contrast_metrics, all_fly_contour_areas, contrast_metric_list_of_lists, fly_contour_area_list_of_lists, morph_open_iteration_number, morph_ellipse_size

    def format_matplotlib_ax_object(self, ax_handle):
        ax_handle.spines['right'].set_visible(False)
        ax_handle.spines['top'].set_visible(False)
        ax_handle.tick_params(direction='out')
        # Only show ticks on the left and bottom spines
        ax_handle.yaxis.set_ticks_position('left')
        ax_handle.xaxis.set_ticks_position('bottom')
        plt.tight_layout()

    def step_through_annotated_output_stack(self,
                                            all_flies_over_time,
                                            all_contrast_metrics,
                                            contrast_metric_list_of_lists,
                                            all_fly_contour_areas,
                                            fly_contour_area_list_of_lists,
                                            timestamp,
                                            output_dir,
                                            video_dir,
                                            analyzed_filename_stack):

        font = cv2.FONT_HERSHEY_SIMPLEX

        number_ive_empirically_determined =2
        all_flies_over_time       =  all_flies_over_time     [0:-1*number_ive_empirically_determined]
        #time_since_release_list   =  time_since_release_list [0:-1*number_ive_empirically_determined]
        analyzed_filename_stack   =  analyzed_filename_stack [0:-1*number_ive_empirically_determined] # these 4 lines are obviously shameful

        flies_on_trap_over_time = np.zeros(len(all_flies_over_time))
        flies_in_trap_over_time = np.zeros(len(all_flies_over_time))
        not_flies_over_time = np.zeros(len(all_flies_over_time))
        seconds_since_release_over_time = np.zeros(len(all_flies_over_time))
        for index, i in enumerate(all_flies_over_time):
            try:
                flies_on_trap_over_time[index]=(len(i['flies on trap']))
                flies_in_trap_over_time[index]=(len(i['flies in trap']))
                not_flies_over_time[index]=(len(i['not_flies']))
                seconds_since_release_over_time[index]=(i['seconds since release'])
            except:
                continue

#        window_size = 10
        window_size = 5

        low_pass_flies_on_trap = np.zeros(len(flies_on_trap_over_time)-window_size)
        low_pass_flies_in_trap = np.zeros(len(flies_on_trap_over_time)-window_size)
        for i in range (window_size, len(flies_on_trap_over_time)):
            low_pass_flies_on_trap[i-window_size] = (np.mean(flies_on_trap_over_time[i-window_size:i]))
            low_pass_flies_in_trap[i-window_size] = (np.mean(flies_in_trap_over_time[i-window_size:i]))

        annotated_frame_filenames = self.get_filenames(path = video_dir, contains = ".jpg", does_not_contain = [])
        print ('now reading in annotated frames and merging them with other graphics')
        for frame_pos, name in enumerate(annotated_frame_filenames):
            display_image = cv2.imread(name)
            plt.close('all') # < ---- dealing with the memory issues of having too many windows open at once
            try:
                filename = analyzed_filename_stack[frame_pos]
                #time_since_release = time_since_release_list[frame_pos]
                time_since_release = seconds_since_release_over_time[frame_pos]
            except:
                break


#            display_image_resized = cv2.resize(display_image, (1296,972)) #halves image dimensions just for display purposes
#            display_image_resized = display_image_resized[:,200:-240].copy()

            
            ## KH,TW TO SEE THE FULL TRAP PIC  7.20.21

            display_image_resized = display_image[:,500:-325].copy()
        #### now plotting the graph of flies over time
#            fig = plt.figure(figsize=(10,9), facecolor="white")
            fig = plt.figure(figsize=(16,16), facecolor="white")
            ax2 = fig.add_subplot(212)

            # proposed_contrast_metric = self.fit_data_to_trimodal(all_contrast_metrics,
            #                                         trimodal_expected,
            #                                         ax_handle = ax2,
            #                                         plot_histogram = True) # <---- THIS SHOULD REEEALLY ONLY HAPPEN ONCE, NOT IN THIS LOOP
            # plt.xlabel('contrast metric (per-pixel fg-bg; avg per contour)')
            # plt.ylabel('count')

            current_frame_contrast_metrics = contrast_metric_list_of_lists[frame_pos]
            current_frame_fly_contour_areas = fly_contour_area_list_of_lists[frame_pos]
            self.plot_2d_scatter(all_contrast_metrics,
                            all_fly_contour_areas,
                            current_frame_contrast_metrics,
                            current_frame_fly_contour_areas,
                            ax_handle = ax2)
            plt.xlabel('contrast metric (per-pixel fg-bg; avg per contour)')
            plt.ylabel('contour area (pixels^2)')

            ax = fig.add_subplot(211)
            ax.scatter(seconds_since_release_over_time, flies_in_trap_over_time, color = [0.6,0,0.6])
            ax.plot(seconds_since_release_over_time[window_size:], low_pass_flies_in_trap, color = [0.6,0,0.6], lw = 2, label = 'in trap')
            ax.scatter(seconds_since_release_over_time, flies_on_trap_over_time, color = 'black')
            ax.plot(seconds_since_release_over_time[window_size:], low_pass_flies_on_trap, color = 'black', lw =2, label = 'on trap')
            legend = ax.legend(loc='upper left', shadow=False) #, fontsize='x-large')
            ax.axvline(x = time_since_release, color = [1.0,0.35,0], lw =2)
            plt.xlabel('seconds since release')
            plt.ylabel('flies in frame')
            self.format_matplotlib_ax_object (ax_handle = ax)
            fig.canvas.draw()
            graph = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
            graph  = graph.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            graph = cv2.cvtColor(graph,cv2.COLOR_RGB2BGR)

            h1, w1 = graph.shape[:2]
            h2, w2 = display_image_resized.shape[:2]
#            h2, w2 = display_image.shape[:2]
            #create empty matrix
            height = max(h1,h2)
            vis = np.zeros((height, 30+w1+w2,3), np.uint8)
            #vis = np.zeros((h1+h2, max(w1, w2),3), np.uint8)
            #combine 2 images

#            pdb.set_trace()
#            vis[150:150+h1, 30:30+w1,:3] = graph
            vis[50:50+h1, 30:30+w1,:3] = graph
            vis[:h2, 30+w1:30+w1+w2,:3] = display_image_resized
#            vis[:h2, 30+w1:30+w1+w2,:3] = display_image
            timestr = filename.split('_')[-1].split('.')[0]
            seconds = str(int(divmod(time_since_release,60)[1]))
            if len(seconds) == 1:
                seconds = '0'+seconds
            textstr = 'timestamp: '+timestr[0:2]+':'+timestr[2:4]+':'+timestr[4:6]+'; time since release: '+ str(int(divmod(time_since_release,60)[0]))+':'+ seconds

            cv2.putText(vis, textstr, (30+w1+60,50), font, 1, (255,255,255),2, cv2.LINE_AA)

            idstr = '~%d flies released at %s ' %(self.field_parameters["estimated_number_of_flies_released"], self.field_parameters['time_of_fly_release'])
            cv2.putText(vis, idstr, (35,50), font, 1, (255,255,255),2, cv2.LINE_AA)
            
            idstr2 = self.trap.split('_')[0]+' ' +self.trap.split('_')[1]+'; %d flies caught' %(self.field_parameters['trap counts'][self.trap])
            cv2.putText(vis,idstr2, (35,90), font, 1, (255,255,255),2, cv2.LINE_AA)

            #now saving into stack
            cv2.imwrite(output_dir + "/%d.jpg" % frame_pos, vis)

        sample_video_str = output_dir+'/'+self.trap + '_analyzed_%d_min_post_release' %(self.min_post_r)+'.mp4'
        output_dir_jpgs = output_dir+"/%d.jpg"
        ##
        ## KH,TW NEED TO FIX 7.19.21 - COMMENTED OUT NOT WORKING
        ##
        #if self.save_video:
            #subprocess.call(["ffmpeg", "-framerate", "3", "-i", output_dir_jpgs, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", sample_video_str])

        if self.calculate_final == True:
            print ('calculating final')
            current_trap_dictionary = {self.trap:{'flies on trap over time:': flies_on_trap_over_time.tolist(),
                                            'flies in trap over time:': flies_in_trap_over_time.tolist(),
                                            'not flies over time:'    : not_flies_over_time.tolist(),
                                            'seconds since release:'  : seconds_since_release_over_time.tolist()}}
            with open(self.directory+'/all_traps_final_analysis_output.json') as f:

                growing_json = json.load(f)
            #add current trap dictionary to growing_json
#            pdb.set_trace()
            growing_json.update(current_trap_dictionary) #CAREFUL; THIS WILL OVERWRITE ANY KEYS THAT ALREADY EXIST IN THE JSON
            with open(self.directory+'/all_traps_final_analysis_output.json', mode = 'w') as f:
                json.dump(growing_json,f, indent = 1)

            fig = plt.figure(figsize=(10,5), facecolor="white")
            ax = fig.add_subplot(111)
            ax.scatter(seconds_since_release_over_time, flies_in_trap_over_time, color = [0.6,0,0.6])
            ax.plot(seconds_since_release_over_time[window_size:], low_pass_flies_in_trap, color = [0.6,0,0.6], lw = 2, label = 'in trap')
            ax.scatter(seconds_since_release_over_time, flies_on_trap_over_time, color = 'black')
            ax.plot(seconds_since_release_over_time[window_size:], low_pass_flies_on_trap, color = 'black', lw =2, label = 'on trap')
            legend = ax.legend(loc='upper left', shadow=False) #, fontsize='x-large')
            plt.xlabel('seconds since release')
            plt.ylabel('flies in frame')
            self.format_matplotlib_ax_object(ax_handle = ax)
            time_string = str(time.time()).split('.')[0] # this is not very human-readable, but helps prevent overwriting
            namestr = self.directory+'/arrival_dynamics_figs/'+self.trap+'_flies_over_time_'+time_string+'.svg'

 #           pdb.set_trace()
            plt.savefig(namestr, bbox_inches='tight')
            pngnamestr = self.directory+'/arrival_dynamics_figs/'+self.trap+'_flies_over_time_'+time_string+'.png'
            plt.savefig(pngnamestr, bbox_inches='tight')
        return output_dir

    def save_all_analysis_parameters(self,
                                    morph_open_iteration_number,
                                    morph_ellipse_size,
                                    mahalanobis_squared_thresh,
                                    output_directory):
        parameter_dictionary = {'minimum_on_trap_contour_size':self.minimum_on_trap_contour_size,
                                'maximum_on_trap_contour_size':self.maximum_on_trap_contour_size,
                                'minimum_in_trap_contour_size':self.minimum_in_trap_contour_size,
                                'maximum_in_trap_contour_size':self.maximum_in_trap_contour_size,
                                'ontrap_intrap_threshold': self.ontrap_intrap_threshold,
                                'smoothing_morph_opening_iterations':morph_open_iteration_number,
                                'smoothing_morph_ellipse_size': morph_ellipse_size,
                                'mahalanobis_squared_thresh': mahalanobis_squared_thresh,
                                'buffer_btw_training_and_test':self.buffer_btw_training_and_test,
                                'number_of_frames_on_which_background_is_trained':self.train_num}
        with open(output_directory+'/analysis_parameters.json', mode = 'w') as f:
            json.dump(parameter_dictionary,f, indent = 1)


    def make_full_mask(self,sample_image):
        '''
        returns a mask where the values are 1
        sample_image is row, col, color
        mask has dimensions row,col
        '''
        [nrows,ncols,colors]=np.shape(sample_image)
        mask=np.int8(np.zeros((nrows,ncols)))
        mask[100:-100,100:-100]=1
#        mask[200:-200,200:-200]=1
        return mask

# --------------------------------------------------------------------------------------------------------
    def run(self):
        timelapse_directory = self.directory +'/trapcam_timelapse/'+self.trap
 

        full_filename_list = self.get_filenames(path = timelapse_directory, contains = "tl", does_not_contain = ['th']) #  full list of image filenames in the folder
        filename_list = ['']*(len(full_filename_list))
  
        image_count = 0

        for filename in full_filename_list:
            time_since_release = self.get_time_since_release_from_filename(name = filename)
            if time_since_release < -60* self.min_prior_to_r:
                continue
            if time_since_release > 60* self.min_post_r:
                break
            filename_list[image_count]= filename
            image_count += 1
        filename_list = filename_list[0:image_count-1] # <----could be off-by-one
#        pdb.set_trace()
#        sample_image =  np.zeros_like(self.load_color_image(filename_list[40]))
        sample_image =  np.zeros_like(self.load_color_image(filename_list[15]))
        if self.USE_FULL_MASK:
            square_mask=self.make_full_mask(sample_image)
        else:
            square_mask = self.load_mask(square_mask_path = timelapse_directory+'/mask.jpg')

        del(full_filename_list)

        
        masked_image_stack = np.stack([sample_image for _ in range(image_count+1)], axis = 0)
        image_count = 0
        for filename in filename_list:
            img = self.load_color_image(filename)
            if img is None:
                print ('img is None!')
                continue
            else:
                masked_image_stack[image_count] = cv2.bitwise_and(img,img,mask = square_mask)
                image_count +=1
        del(img)

        

        print ('length of masked image stack: '+str(len(masked_image_stack)))

        timestamp = str(int(time.time())) +'_mahal'+str(self.mahalanobis_squared_thresh) +'_trainnum'+str(self.train_num)
        annotated_frame_dir = self.directory+'/'+self.trap+'_videos/'+timestamp+'/annotated_frames/'
        subprocess.call(['mkdir', '-p', annotated_frame_dir])

        all_flies_over_time, time_since_release_list, analyzed_filename_stack, all_contrast_metrics, all_fly_contour_areas, contrast_metric_list_of_lists, fly_contour_area_list_of_lists, morph_open_iteration_number, morph_ellipse_size =self.find_contours_using_pretrained_backsub_MOG2(full_image_stack = masked_image_stack,
                                                                            filename_stack = filename_list,
                                                                            video_dir = annotated_frame_dir)

        ########### NOW TO STEP THROUGH FRAMES IN ANNOTATED_OUTPUTSTACK
        del(masked_image_stack) # <--- if I'm properly managing references to masked_image_stack, this shouldn't really be necessary

        #save all_contrast_metrics so I can play around with curve fitting
        contrast_metric_dictionary = {'all contrast metrics': all_contrast_metrics.tolist()}
        with open(self.directory+'/all_contrast_metrics/'+self.trap+'.json', mode = 'w') as f:
            json.dump(contrast_metric_dictionary,f, indent = 1)

        annotated_frames_plus_graphs_dir = self.directory+'/'+self.trap+'_videos/'+timestamp+'/annotated_frames_plus_graphs'
        subprocess.call(['mkdir', annotated_frames_plus_graphs_dir])

        output_directory = self.step_through_annotated_output_stack(all_flies_over_time,
                                                all_contrast_metrics,
                                                contrast_metric_list_of_lists,
                                                all_fly_contour_areas,
                                                fly_contour_area_list_of_lists,
                                                timestamp,
                                                annotated_frames_plus_graphs_dir,
                                                annotated_frame_dir,
                                                analyzed_filename_stack)

        # if calculate_threshold:
        #     proposed_contrast_metric = self.fit_data_to_trimodal(all_contrast_metrics, trimodal_expected, ax_handle = None, plot_histogram = False)
        #
        # if proposed_contrast_metric is not None:
        #     if proposed_contrast_metric.size != 0:
        #         print ('proposed contrast cutoff: '+ str(proposed_contrast_metric))
        #         if calculate_threshold:
        #             with open(self.directory+'/all_traps_gaussian_analysis_params.json') as f:
        #                 growing_json = json.load(f)
        #             growing_json[self.trap]['fixed in-trap on-trap threshold'] = int(round(proposed_contrast_metric))
        #             with open(self.directory+'/all_traps_gaussian_analysis_params.json', mode = 'w') as f:
        #                 json.dump(growing_json,f, indent = 4)

        self.save_all_analysis_parameters(morph_open_iteration_number= morph_open_iteration_number,
                                        morph_ellipse_size = morph_ellipse_size,
                                        mahalanobis_squared_thresh = self.mahalanobis_squared_thresh,
                                        output_directory = output_directory)

        cv2.destroyAllWindows()