# -*- coding: utf-8 -*-
"""

Created on Thu Nov 14 14:26:26 2013

test function for HEXTIC_cal class

@author: wong
"""
#%% variable initialization  

file_name = "HEXITEC_CalTable.dat"
w_file_name = "Caldata.dat"

# image row and colun size   
im_r = 80
im_c = 80
num_im = 2

# sigma threhold variable
sigma = 3;

#%% read data from HEITEC calbration dat
io_tab = HEXTIC_data_rw()
io_tab.read_image(file_name, im_r, im_c, num_im)
raw_arr = io_tab.raw_dat
print(raw_arr[0,0])    
print(raw_arr[1,0])    


#%% calculate mean and variance 
cal_tab = HEXTIC_cal(raw_arr)
cal_tab.image_cal(sigma)
mean_arr = cal_tab.mean_arr
std_arr = cal_tab.std_arr
tre_arr = mean_arr + sigma*std_arr

print(mean_arr[0])       
print(std_arr[0])
 
#%% write binary file using cal_tab
io_tab.write_image(w_file_name, tre_arr)