from PIL import Image
from functions import stgPrb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

def stgPrb(martix): # 计算卡方
    count = np.zeros(256,dtype=int)
    for i in range(len(martix)):
        for j in range(len(martix[0])):
            count[martix[i][j]] += 1
    h2i = count[2:255:2]
    h2is = (h2i+count[3:256:2])/2
    filter= (h2is!=0)
    k = sum(filter)
    idx = np.zeros(k,dtype=int)
    for i in range(127):
        if filter[i]==True:
            idx[sum(filter[1:i])]=i
    r = sum(((h2i[idx]-h2is[idx])**2)/(h2is[idx]))
    p = 1-chi2.cdf(r,k-1)
    return p

def main():
    #lsb 隐写
    p = 0.0
    blk_count = 0
    img_lsb = Image.open("./test/zzh2.bmp")
    martix = np.array(img_lsb)

    for i in range(0,int(img_lsb.size[0]/10)- 1):
        for j in range(int(img_lsb.size[1]/10) - 1):
            p = stgPrb(martix[10*j:10*(j+1),10*i:10*(i+1)])
            if p > 0.999:
                blk_count = blk_count + 1
    print(blk_count)
main()