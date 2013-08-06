import struct
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from struct import *
from numpy import *

def readi(f,n):        
    try:
        return struct.unpack('%di' %n,f.read(4*n))
    except:
        return ()

newexposure = hexitec_exposure()

f = open("HEXITEC_CalTable.dat","rb")
newval = readi(f,1)
while len(newval) == 1:
    newexposure.caldata.send(newval[0])
    newval = readi(f,1)
newexposure.caldata.close()
f.close()
f = open("Science_Output.dat","rb")
newval = readi(f,1)
while len(newval) == 1:
    newexposure.imgdata.send(newval[0])
    newval = readi(f,1)
newexposure.imgdata.close()
f.close()

subplot(2,1,1)
imgplot = plt.imshow(newexposure.samples[0],aspect='equal')
subplot(2,1,2)
(x,y) = histogram(newexposure.samples[0:newexposure.validimages],bins=2000,range=(9000,13000))
bar(y[0:2000],x[0:2000])

''' this is the old version of this program (didn't utilize exposure object)
def dec2bin(n,m):
    x = zeros(m,int);
    for i in range(0,m):
        x[i] = (n//(2**i))%2;
    return x;
                    
images = zeros((100,80,80),int);
timestamps = zeros(100,int);
rowbufIDs = zeros((100,80),int);
rowIDs = zeros((100,80),int);    #initializing data structures
mask = zeros((100,80,80),int);
rawflags = zeros((100,80),int);
inbuffer = zeros(20,int);
f = open("Science_Output.dat","rb");
for i in range(0,2):
    inbuffer[0:4] = readi(f,4);
    #timestamps[i] = (buffer[1]%(2**16)) * 2**32 + (buffer[2]%(2**16)) * 2**16 + buffer[3];  #need to solve overflow error...
    for r in range(0,80):
         inbuffer[0:9] = readi(f,9);
         rowbufIDs[i][r] = inbuffer[0] // 2**10;
         rowIDs[i][r] = inbuffer[0] % 2**8;
         rawflags[i][r] = (inbuffer[0] // 2**8) % 2;
         mask[i][r][14:20] = dec2bin(inbuffer[1]%(2**6),6);
         mask[i][r][0:14] = dec2bin(inbuffer[2]%(2**14),14);
         mask[i][r][34:40] = dec2bin(inbuffer[3]%(2**6),6);
         mask[i][r][20:34] = dec2bin(inbuffer[4]%(2**14),14);
         mask[i][r][54:60] = dec2bin(inbuffer[5]%(2**6),6);
         mask[i][r][40:54] = dec2bin(inbuffer[6]%(2**14),14);
         mask[i][r][74:80] = dec2bin(inbuffer[7]%(2**6),6);
         mask[i][r][60:74] = dec2bin(inbuffer[8]%(2**14),14);
         for c in range(0,80):
             if mask[i][r][c] == 1:
                 inbuffer[0:1] = readi(f,1);
                 images[i][r][c] = inbuffer[0] + (384 * (1 - rawflags[i][r]));
    readi(f,1);
f.close();'''
