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
        #implement some error rejection capability into the loadimagedata routine
        #possibly methods for converting to hyperspectral image and simple spectrum
        #come up with a way to dynamically scale this object to handle n- datastreams (perhaps an "addition" method or something)
    #def __new__(self):
        #pass
    
    def __init__(self):
        self.validimages = 0        
        self.samples = zeros((1000,80,80),int)
        self.timestamps = zeros(1000,long)
        self.rowbufIDs = zeros((1000,80),int)
        self.rowIDs = zeros((1000,80),int)
        self.mask = zeros((1000,80,80),bool)
        self.rawflags = zeros((1000,80),int)
        self.endsync = zeros(1000,int)
        self.caltable = zeros((80,80),int)
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
                for g in range (0,141,20):             
                    newcaltable[r][c+g] = (yield)
        self.caloffset = newcaloffset
        self.caltable = newcaltable
        while 1:
            (yield)
            
    def loadimagedata(self):
        inbuffer = zeros(17,long)
        while 1:
            while (yield) != 0xFE6B:  #search for sync pattern
                pass
            for b in range(0,3):
                inbuffer[b] = (yield)
                print inbuffer[b]%(2**16) << 16
            self.timestamps[self.validimages] = ((inbuffer[0]%(2**16)) << 32) + ((inbuffer[1]%(2**16)) << 16) + (inbuffer[2]%(2**16))
            for r in range(0,80):
                for b in range(0,9):
                    inbuffer[b] = (yield)
                self.rowbufIDs[self.validimages][r] = (inbuffer[0] & 0x3c00) >> 10
                self.rowIDs[self.validimages][r] = inbuffer[0] & 0x00ff
                self.rawflags[self.validimages][r] = (inbuffer[0] & 0x0100) >> 8
                for g in range(0,8,2):
                    self.mask[self.validimages][r][(14+(10*g)):(20+(10*g))] = dec2bin(inbuffer[1+g]%(2**6),6)   #need a more efficient way to handle these masks
                    self.mask[self.validimages][r][(0+(10*g)):(14+(10*g))] = dec2bin(inbuffer[2+g]%(2**14),14)
                for c in range(0,80):
                    if self.mask[self.validimages][r][c] == 1:
                        inbuffer[0] = (yield)
                        self.samples[self.validimages][r][c] = inbuffer[0] + ((self.caloffset + self.caltable[r][c]) * (1 - self.rawflags[self.validimages][r]))
            self.endsync[self.validimages] = (yield)
            self.validimages += 1
            