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

class hexitec_image:  #need to implement a way to copy images or create new images... python is a bit strange with the way it copies objects...
    samples = zeros((80,80),int)
    rowbufIDs = zeros(80,int)
    rowIDs = zeros(80,int)
    mask = zeros((80,80),int)   #need to come up with a better representation for masks... this approach is clearly wasteful
    rawflags = zeros(80,int)
    endsync = 0
    def reset(self):
        self.samples = zeros((80,80),int)
        self.rowbufIDs = zeros(80,int)
        self.rowIDs = zeros(80,int)
        self.mask = zeros((80,80),int)
        self.rawflags = zeros(80,int)
        self.endsync = 0
    
class hexitec_exposure:
    images = []
        #TO DO:  add member functions for the following activities:
        #export calibration table
        #export data set
        #generate calibration table (from data)
        #possibly methods for converting to hyperspectral image and simple spectrum
    def _init_(self):
        self.images = []
        self.caltable = zeros((80,80),int)
        self.caloffset = 0;
        
    def loadcaltable(self):
        newcaltable = zeros((80,80),int)        
        newcaloffset = (yield)
        for r in range (0,80):
            for c in range (0,20):
                newcaltable[r][c+60] = (yield)
                newcaltable[r][c+40] = (yield)
                newcaltable[r][c+20] = (yield)
                newcaltable[r][c] = (yield)
        self.caloffset = newcaloffset
        self.caltable = newcaltable
        while 1:
            (yield)
            
    def unpack(self):
        inbuffer = zeros(9,int)
        newimage = hexitec_image()
        while 1:
            while (yield) != 0xFE6B:  #search for sync pattern
                pass
            for b in range(0,3):
                inbuffer[b] = (yield)
            #this timestamps
            #timestamps[i] = (buffer[1]%(2**16)) * 2**32 + (buffer[2]%(2**16)) * 2**16 + buffer[3]  #need to solve overflow error...
            for r in range(0,80):
                for b in range(0,9):    
                    inbuffer[b] = (yield)
                newimage.rowbufIDs[r] = (inbuffer[0] & 0x3c00) >> 10
                newimage.rowIDs[r] = inbuffer[0] & 0x00ff
                newimage.rawflags[r] = (inbuffer[0] & 0x0100) >> 8
                newimage.mask[r][14:20] = dec2bin(inbuffer[1]%(2**6),6)   #need a more efficient way to handle these masks
                newimage.mask[r][0:14] = dec2bin(inbuffer[2]%(2**14),14)
                newimage.mask[r][34:40] = dec2bin(inbuffer[3]%(2**6),6)
                newimage.mask[r][20:34] = dec2bin(inbuffer[4]%(2**14),14)
                newimage.mask[r][54:60] = dec2bin(inbuffer[5]%(2**6),6)
                newimage.mask[r][40:54] = dec2bin(inbuffer[6]%(2**14),14)
                newimage.mask[r][74:80] = dec2bin(inbuffer[7]%(2**6),6)
                newimage.mask[r][60:74] = dec2bin(inbuffer[8]%(2**14),14)
                for c in range(0,80):
                    if newimage.mask[r][c] == 1:
                        inbuffer[0] = (yield)
                        newimage.samples[r][c] = inbuffer[0] + ((self.caloffset + self.caltable[r][c]) * (1 - rawflags[i][r]))
            newimage.endsync = (yield)
            self.images.append(newimage)
            newimage.reset()