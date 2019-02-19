import smbus
import math
import time
import os
import json
import matplotlib
#matplotlib.use("AGG")
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from pymongo import MongoClient


client= MongoClient('localhost',27017)


db = client.test_database

#Register
power_mgmt_1 = 0x6b

#COEFFICIENTS_HIGH_05_HZ = [1,-1.905384612118461,0.910092542787947,0.953986986993339,-1.907503180919730,0.953986986993339]
COEFFICIENTS_HIGH_05_HZ = [1,-1.905384612118461,0.910092542787947,0.953986986993339,-1.907503180919730,0.953986986993339]

def __init__(self):
    pass

def fil(data,c = COEFFICIENTS_HIGH_05_HZ):
    f_d = [0,0]
    for i in range(2,len(data)):
        f_d.append(c[0] * (data[i]* c[3] + data[i-1] * c[4] + data[i-2] * c[5] - f_d[i-1] * c[1] - f_d[i-2] * c[2]))
    return f_d
    
def read_byte(reg):
    return bus.read_byte_data(ad,reg)

def read_word(reg):
    h = bus.read_byte_data(ad,reg)
    l = bus.read_byte_data(ad,reg+1)
    value = (h<<8)+l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if(val >= 0x8000):
        return -((65535-val)+1)
    else:
        return val

def dist(a,b,c):
    return math.sqrt((a*a)+(b*b)+(c*c))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y,dist(x,z))
    return math.degrees(radians)

def do_sma(k,i):
    if i==0 :
        return k[0]
    elif i== len(k)-1:
        return k[i]
    first = (k[i-1]+k[i])/2
    second = (k[i]+k[i+1])/2
    third = (k[i-1]+k[i+1])/2
    return (first+second+third)/3
    
bus = smbus.SMBus(1)
ad = 0x68
bus.write_byte_data(ad,power_mgmt_1,0)
data = []
sampling = 0.025
print("\033c")
raw_input("Start ")
startTime = time.time()
time.sleep(sampling)
try:
    while(True):
        measureTime = time.time() - startTime
        print ("Time : ", measureTime)  
        acc_x = read_word_2c(0x3b) / 16384.0
        acc_y = read_word_2c(0x3d) / 16384.0
        acc_z = read_word_2c(0x3f) / 16384.0
        
        
        print("Acc X : " ,  acc_x)
        print("Acc Y : " ,  acc_y)
        print("Acc Z : " ,  acc_z)
        data.append([measureTime,acc_x,acc_y,acc_z])
        
        time.sleep(sampling)

        print("\033c")
        
except KeyboardInterrupt:
    t = []
    x = []
    y = []
    z = []
    sma = []
    mag = []
    for val in data:
        t.append(val[0])
        x.append(val[1])
        y.append(val[2])
        z.append(val[3])

    x = fil(x)
    y = fil(y)
    z = fil(z)
    for i in range(0,len(x)):
        mag.append(dist(x[i],y[i],z[i]))
    for i in range (0,len(mag)):
        sma.append(do_sma(mag,i))
    plt.subplot(311)
    plt.xlabel('Time [t]')
    plt.plot(t,x)
    plt.plot(t,y)
    plt.plot(t,z)
    plt.legend(['x','y','z'])
    plt.ylim(-1.2,1.2)
    plt.subplot(312)
    plt.xlabel('Time [t]')
    plt.ylim(0,2)
    plt.plot(t,mag)
    plt.legend(['mag'])
    plt.subplot(313)
    plt.xlabel('Time [t]')
    plt.ylim(0,2)
    plt.plot(t,sma)
    plt.legend(['sma'])
    #plt.show()
    MAG = {'Mag' : mag}
    SMA = {"SMA" : sma}

    '''
    fft_mag = fft(mag)
    plt.subplot(313)
    plt.plot(fft_mag)
    plt.xlabel('Freq [Hz]')
    plt.ylabel('Amplitude')
    plt.legend(['fft'])
    '''
    path = "JA/"
    for i in range (1,100):
            s = path+"fig("+str(i)+").png"
            exists =  os.path.isfile(s)
            if exists==False :
                txt_s = path+"data("+str(i)+").txt"
                txt = open(txt_s,"a")
                txt.write("t" + json.dumps(t))
                txt.write("\n")
                txt.write("MAG " + json.dumps(mag))
                txt.write("\n")
                txt.write("SMA " + json.dumps(sma))
                txt.close()
                s = path+"fig("+str(i)+").png"
                print(s)
                plt.savefig(s)
                break
          
    pass

