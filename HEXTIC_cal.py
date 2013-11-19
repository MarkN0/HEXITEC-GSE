# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:51:39 2013

HEXTIC calibration data mean and std calculation
HEXTIC_cal(data)
inputs:
    data: data to be calculate with sum and variance
    
-------------------------------------------------------------------------------

function: *.image_cal()  
calculate mean and std from the data file
  
outputs: 
    *.mean_arr: mean of the cal table (size, [1, im_r x im_c])
    *.std_arr: standard deviation of the cal table (size, [1, im_r x im_c])
    
-------------------------------------------------------------------------------


@author: wong
"""

import numpy

class HEXTIC_cal:
    #%% class initializaiton
    def __init__(self, data): 
        
        mat_size = numpy.shape(data)
        im_size = mat_size[1]  
        num_im = mat_size[0]
        
        self.im_size = im_size
        self.num_im = num_im
        self.data = data
        self.mean_arr = numpy.zeros(im_size)
        self.std_arr = numpy.zeros(im_size)
        self.tre_arr = numpy.zeros(im_size)
        
    #%% calibration image mean and variance calibration
    def image_cal(self, sigma):
                
        dat = self.data
        
        sum1_arr = numpy.sum(dat, axis=0)
        sum2_arr = numpy.sum(dat**2, axis=0)   

        mean_arr = sum1_arr/self.num_im      
        std_arr = ((sum2_arr/self.num_im-((sum1_arr/self.num_im)**2)))**0.5
         
        self.mean_arr = mean_arr
        self.std_arr = std_arr
        self.tre_arr = mean_arr + sigma*std_arr
        
    
    