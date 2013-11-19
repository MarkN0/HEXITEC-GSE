import struct
import numpy

# import plotting library
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from struct import *
from numpy import *

# define read file function
def readi(f,n):        
    try:
        return struct.unpack('%di' %n,f.read(4*n))
    except:
        return ()

# call hexitec_exposure class
newexposure = hexitec_exposure()

 # file read
f = open("HEXITEC_CalTable.dat","rb")
newval = readi(f,1)

while len(newval) == 1:
    newexposure.caldata.send(newval[0])
    newval = readi(f,1)
newexposure.caldata.close()

f.close()

# file read
f = open("Science_Output.dat","rb")
newval = readi(f,1)
while len(newval) == 1:
    newexposure.imgdata.send(newval[0])
    newval = readi(f,1)
newexposure.imgdata.close()
f.close()

# plot read data
subplot(2,1,1)
cla()
imgplot = plt.imshow(newexposure.samples[0],aspect='equal')
plt.colorbar()
subplot(2,1,2)
cla()
rmin = min(newexposure.samples[(newexposure.mask>0)])
rmax = max(newexposure.samples[(newexposure.mask>0)])
nbins = (rmax-rmin)/2
(x,y) = histogram(newexposure.samples[0:newexposure.validimages],bins=nbins,range=(rmin,rmax))
bar(y[0:nbins],x[0:nbins])
