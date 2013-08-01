from numpy import *

def readi(f,n):        
    #x = zeros(n,int);    
    #for i in range(0,n):
        #x[i] = struct.unpack('i',f.read(4))[0];
    return struct.unpack('%di' %n,f.read(4*n))[0];

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
f.close();
