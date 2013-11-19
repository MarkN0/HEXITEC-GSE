# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:09:22 2013

@author: mewong

HEXTIC dat file reading and writing function
HEXTIC_data_rw()

-------------------------------------------------------------------------------

function: *. read_image(file_name, im_r, im_c, num_im)
read binary file from image data

inputs:
    file_name: file input name
    im_r: image row
    im_c: image column
    num_im: number of image to be used for calcuation
outpus:
    *.raw_dat: raw data read from file name in numpy matrix (size, [num_im, im_r x im_c]) 

-------------------------------------------------------------------------------

function: *.write_image(w_file_name, cal_arr):
save calbration data to a binary file

inputs:
    w_file_name: file name to be written
    cal_arr : array in int to be written into binary file
outputs:
    binary file in the local directory with name, w_file_name
    
-------------------------------------------------------------------------------
notes:

1. The file is assumed from HEXTIC calibration data where the first x number of
    samples are for the 1st image and followed by the second image
    
-------------------------------------------------------------------------------


"""

import struct
import numpy

class HEXTIC_data_rw:
    #%% class initializaiton
    def __init__(self): 
           
        self.raw_dat = []
        
    #%% Raw data capture    
    def read_image(self, file_name, im_r, im_c, num_im):
        
        total_pix = im_r*im_c*num_im
        arr = numpy.zeros(total_pix)  
        
        with open(file_name,"rb") as f:
                        
            for i in range(0, total_pix-1):  
                dat = struct.unpack('%di' %1, f.read(4))
                arr[i] = dat[0]
        
        self.raw_dat = arr.reshape((num_im, (im_r*im_c)))
        
    #%% write threshold data to file
    def write_image(self, w_file_name, cal_arr):
        
        with open(w_file_name,"wb") as f:
            w_bf = bytearray(cal_arr)
            f.write(w_bf)
        
        print "File '",w_file_name,"' complete!"