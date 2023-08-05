# _*_ coding:UTF-8 _*_

# Author: Bing Shi
# Institution: City University of Hong Kong
# Date: 2017.4~2018.3
# Function： Generate g1 and g2, then make features of them. 
# Using:

import  os
import  sys
import  copy
import  math
import  matplotlib.pyplot as plt
import  numpy as np  
from  numpy import random as nr

# === setting of parameter ===
k = 10                 

samples_num = 100
outliers_num = 5
sigma = 0.1  
mu = 0

def gengraph(f1, f2, samples_num = samples_num, outliers_num = outliers_num, sigma = sigma, mu = mu):    
    np.set_printoptions(precision=3)
    randArray = nr.random(size=(samples_num, 2))*500               # G1   
    secondArray = copy.deepcopy(randArray)                         # G2
    if sigma != 0:
        deformationArray = nr.normal(mu, sigma, size=(samples_num, 2))*50  
        secoArray = secondArray + deformationArray 
    if outliers_num != 0:    
        outlierArray = nr.random(size=(outliers_num, 2))*500  
        secoArray = np.vstack((secondArray, outlierArray))    

    np.savetxt(f1, randArray, fmt='%.4f %.4f', newline='\r\n')     # save data
    np.savetxt(f2, secoArray, fmt='%.4f %.4f', newline='\r\n')
    return (randArray, outlierArray, deformationArray, secoArray)
#end

def drawgraph(randArray, outlierArray, deformationArray, secoArray):    
    ''' plot scatter    #matplotlib.rc('font', size=6) '''
    plt.subplot(141)
    plt.title('G1')
    plt.plot(randArray[:,0], randArray[:,1],'+')           
 
    plt.subplot(142)
    plt.title('Outlier')
    plt.plot(outlierArray[:,0], outlierArray[:,1],'+')    
    
    plt.subplot(143)
    plt.title('Deformation')
    plt.plot(deformationArray[:,0], deformationArray[:,1],'+')    
    
    plt.subplot(144)
    plt.title('G2')
    plt.plot(secoArray[:,0], secoArray[:,1],'+')
    
    plt.savefig('g1g2.png', dpi=125)    
    plt.show()  
#end

def makefeatures(fn):
    mname, ext = os.path.splitext(fn)
    points = np.loadtxt(fn, dtype=np.float32)        #load keypoints
    n = points.shape[0]
    print('Row: %d'%n)
    x1, x2 = np.meshgrid(points[:, 0], points[:, 0])
    y1, y2 = np.meshgrid(points[:, 1], points[:, 1])
    deltax = x2-x1
    deltay = y2-y1
    distances=np.sqrt(deltax**2 + deltay**2)
    neighbours = distances.argsort()  
    features = []
    for i in range(n):
        index = neighbours[i][1:k]
        print('%d:\nindex:'%i, end=' ');   print(index)
        d = distances[i][index]
        print('distances: ', end=' ');     print(d)
        min=np.min(d);   assert min==distances[i][neighbours[i][1]]
        max=np.max(d);   assert max==distances[i][neighbours[i][k-1]]
        mean=np.mean(d)  
        std=np.std(d)
        median=np.median(d)
        p1=np.percentile(d,25)
        p3=np.percentile(d,75)
        f,bins = np.histogram(d,bins=[min, p1, median, p3, max])          #f:frequency
        feat=[10*min/max, 10*mean/max, 10*std/max]                        #feat = feat + list(f)
        print('near,far: %d %d'%(neighbours[i][1], neighbours[i][k-1]))
        x=[deltax[i][neighbours[i][1]], deltay[i][neighbours[i][1]]]
        y=[deltax[i][neighbours[i][k-1]], deltay[i][neighbours[i][k-1]]]
        lx=np.sqrt(np.dot(x, x))
        ly=np.sqrt(np.dot(y, y))
        cos_angle=np.dot(x, y)/(lx*ly)
        cos_angle = np.maximum(-1,cos_angle)
        cos_angle = np.minimum(1,cos_angle)
        angle=np.arccos(cos_angle)
        feat.append(angle)
        features.append(feat)
        print(feat)
    features = np.array(features)   
    np.savetxt(mname+'.des.txt', features, fmt="%f", delimiter=' ', newline='\r\n') 
    plt.hist(features)       
    plt.show()
#end 

if __name__=='__main__':  
    (ra, oa, da, sa) = gengraph('g1.txt', 'g2.txt')
    drawgraph(ra, oa, da, sa)
    makefeatures('g1.txt')
    makefeatures('g2.txt')
