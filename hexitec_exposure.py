# -*- coding: utf-8 -*-
"""
Created on Fri Aug 02 12:18:44 2013

@author: kgregory
"""
import copy
from numpy import *

def dec2bin(n,m):     #need to do away with this function (see masks below)
    x = zeros(m,int);
    for i in range(0,m):
        x[i] = (n//(2**i))%2;
    return x;


class test_class:
    def __init__(self):
        self.y = []
        self.data = self.begin()
        self.data.next()
    
    def begin(self):
        for i in range(0,10):
            self.y.append((yield))
        print self.y


class hexitec_exposure:
    #images = []
        #TO DO:  add member functions for the following activities:
        #export calibration table
        #export data set
        #generate calibration table (from data)
        #possibly methods for converting to hyperspectral image and simple spectrum
        #come up with a way to dynamically scale this object to handle n asics
    #def __new__(self):
        #pass
    
    def __init__(self):
        self.validimages = 0        
        self.samples = zeros((1000,80,160),int)
        self.rowbufIDs = zeros((1000,80),int)
        self.rowIDs = zeros((1000,80),int)
        self.mask = zeros((1000,80,160),bool)
        self.rawflags = zeros((1000,80),int)
        self.endsync = zeros(1000,int)
        self.caltable = zeros((80,160),int)
        self.caloffset = 0;
        
        self.caldata = self.loadcaltable()
        self.caldata.next()
        self.imgdata = self.loadimagedata()
        self.imgdata.next()
        
    def loadcaltable(self):
        newcaltable = zeros((80,160),int)        
        newcaloffset = (yield)
        for r in range (0,80):
            for c in range (0,20):
                newcaltable[r][c] = (yield)
                newcaltable[r][c+20] = (yield)
                newcaltable[r][c+40] = (yield)
                newcaltable[r][c+60] = (yield)
                newcaltable[r][c+80] = (yield)
                newcaltable[r][c+100] = (yield)
                newcaltable[r][c+120] = (yield)
                newcaltable[r][c+140] = (yield)
        self.caloffset = newcaloffset
        self.caltable = newcaltable
        while 1:
            (yield)
            
    def loadimagedata(self):
        inbuffer = zeros(17,int)
        while 1:
            while (yield) != 0xFE6B:  #search for sync pattern
                pass
            for b in range(0,3):
                inbuffer[b] = (yield)
            #this timestamps
            #timestamps[i] = (buffer[1]%(2**16)) * 2**32 + (buffer[2]%(2**16)) * 2**16 + buffer[3]  #need to solve overflow error...
            for r in range(0,80):
                for b in range(0,17):    
                    inbuffer[b] = (yield)
                self.rowbufIDs[self.validimages][r] = (inbuffer[0] & 0x3c00) >> 10
                self.rowIDs[self.validimages][r] = inbuffer[0] & 0x00ff
                self.rawflags[self.validimages][r] = (inbuffer[0] & 0x0100) >> 8
                self.mask[self.validimages][r][14:20] = dec2bin(inbuffer[1]%(2**6),6)   #need a more efficient way to handle these masks
                self.mask[self.validimages][r][0:14] = dec2bin(inbuffer[2]%(2**14),14)
                self.mask[self.validimages][r][34:40] = dec2bin(inbuffer[3]%(2**6),6)
                self.mask[self.validimages][r][20:34] = dec2bin(inbuffer[4]%(2**14),14)
                self.mask[self.validimages][r][54:60] = dec2bin(inbuffer[5]%(2**6),6)
                self.mask[self.validimages][r][40:54] = dec2bin(inbuffer[6]%(2**14),14)
                self.mask[self.validimages][r][74:80] = dec2bin(inbuffer[7]%(2**6),6)
                self.mask[self.validimages][r][60:74] = dec2bin(inbuffer[8]%(2**14),14)
                self.mask[self.validimages][r][94:100] = dec2bin(inbuffer[9]%(2**6),6)   #need a more efficient way to handle these masks
                self.mask[self.validimages][r][80:94] = dec2bin(inbuffer[10]%(2**14),14)
                self.mask[self.validimages][r][114:120] = dec2bin(inbuffer[11]%(2**6),6)
                self.mask[self.validimages][r][100:114] = dec2bin(inbuffer[12]%(2**14),14)
                self.mask[self.validimages][r][134:140] = dec2bin(inbuffer[13]%(2**6),6)
                self.mask[self.validimages][r][120:134] = dec2bin(inbuffer[14]%(2**14),14)
                self.mask[self.validimages][r][154:160] = dec2bin(inbuffer[15]%(2**6),6)
                self.mask[self.validimages][r][140:154] = dec2bin(inbuffer[16]%(2**14),14)
                for c in range(0,160):
                    if self.mask[self.validimages][r][c] == 1:
                        inbuffer[0] = (yield)
                        self.samples[self.validimages][r][c] = inbuffer[0] + ((self.caloffset + self.caltable[r][c]) * (1 - self.rawflags[self.validimages][r]))
            self.endsync[self.validimages] = (yield)
            self.validimages += 1
            