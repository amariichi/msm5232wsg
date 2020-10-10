# -*- coding: utf-8 -*-
import os
import sys
import datetime
import struct
import wave
import numpy as np
from scipy.stats import norm
from decimal import Decimal, ROUND_HALF_UP
#import matplotlib.pyplot as plt

def argumentsparser():
    usage = "Usage: python {} any\".fxb\"file".format(__file__)
    arguments = sys.argv
    if len(arguments) == 1 or len(arguments) > 2:
        return usage
    arguments.pop(0)
    if not arguments[0].endswith('.fxb') or arguments[0].startswith('-'):
        return usage

if __name__ == '__main__' :
    if argumentsparser() is None :

        # normal distribution curve is used to simulate msm5232 output volume.        
        def dist(x):
            func = norm.pdf(x,1,5.8)*4000-23
            return func

        # an alternative curve
        #def tanh(x):
        #    a = 3
        #    b = 6.4/15
        #    tanh = ((np.exp(a - b*(x)) - 1)/(np.exp(a - b*(x)) + 1)/((np.exp(a)-1)/(np.exp(a)+1)) + 1)*100
        #    return tanh
        
        def wav1(x):
            xx = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
            flip = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
            ans = flip[x]*dist(xx[x])
            return ans
        
        def wav2(x):
            xx = np.array([0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7])
            flip = np.array([-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.6
            return ans
        
        def wav4(x):
            xx = np.array([0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3])
            flip = np.array([-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.5
            return ans
        
        def wav8(x):
            xx = np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
            flip = np.array([-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1])
            ans = flip[x]*dist(xx[x])
            ans = ans*0.45
            return ans
        
        def switch(num: int, n: int):
            if num & (1 << n):
                return 1
            return 0

        now = datetime.datetime.now()
        dirname = "{0:%y%m%d%H%M%S}".format(now)
        os.makedirs(dirname, exist_ok=True)
        fout1 = open(dirname + "/MSM5232likeWaveTable.fxb", mode="wb")

        fin = open(sys.argv[0], mode="rb")
        fin.seek(0)
        fxbheader = fin.read(156)
        fin.seek(156)
        fxpheader = fin.read(28)
        fin.close()

        zerosixteen = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        ardrslrr = b'\x3F\x72\xF2\xF3\x3D\x90\x90\x91\x3F\x02\x82\x83\x3D\x80\x80\x81'
        eightbits = b'\x3F\x80\x00\x00'
        filtervalue = b'\x3D\x04\x21\x08'

        #------fxb header output------
        fout1.write(fxbheader)

        x = np.arange(32)
        y = np.empty(32,dtype="int64")
        
        for i in range(1,16):
            for j in range(32):
                y[j] = switch(i,0)*wav1(j) + switch(i,1)*wav2(j) + switch(i,2)*wav4(j) + switch(i,3)*wav8(j)
            y = y * 127/max(max(y),-min(y))
            y = np.round(y)
            #print(y)
            #plt.bar(x,y)
            #plt.show()
            y = y + 127
            list = y.astype(np.int64).tolist()

            #------fxp output------
            fout1.write(fxpheader)
            if i > 9 :
                number = i + 1
            else:
                number = i
            tablename = "MSM5232Tbl-".encode('utf-8', 'replace').hex() + str(number + 30)
            fout1.write(bytes.fromhex(tablename))
            fout1.write(zerosixteen)
            fout1.write(ardrslrr)
            fout1.write(eightbits)
            fout1.write(filtervalue)
            for j in range(32):
                fout1.write(struct.pack(">f", list[j]/254))

            #------wave for ELZ_1 output------
            fout2 = wave.Wave_write(dirname + "/" + "MSM5232Table" + "{0:02d}".format(i) + ".wav")
            fout2.setparams((
                1,                 # mono
                1,                 # 8 bits = 1 byte
                48000,             # sampling bitrate
                32,                # samples
                "NONE",            # not compressed
                "not compressed"   # not compressed
                ))
            for j in range(32):
                fout2.writeframesraw(struct.pack("B", int(Decimal(list[j]/254*255).quantize(Decimal('0'), rounding=ROUND_HALF_UP))))
            fout2.close()

        # dummy data of 16th fxp for the fxb file.
        fout1.write(fxpheader)
        tablename = "MSM5232dummy".encode('utf-8', 'replace').hex()
        fout1.write(bytes.fromhex(tablename))
        fout1.write(zerosixteen)
        fout1.write(ardrslrr)
        fout1.write(eightbits)
        fout1.write(filtervalue)
        for i in range(32):
            fout1.write(struct.pack(">f", 0.49803921))
        fout1.close()
 
        print("\n\"MSM5232likeWaveTable.fxb\" for chip32 VSTi is created in the", dirname, "folder successfully.")
        print("Simultaneously 15 wave files are created in the same folder.")
        print("The format is monoral, 8-bit, 48kHz and 32 samples.\nThose wave files are expected to be readable for an ELZ_1 synthesizer.")
           
    else: 
        print(argumentsparser())
