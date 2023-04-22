from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def main():
    plt.figure("pixel")
    img_gray = Image.open("./test/zzh.bmp").convert("L")
    img_lsb = Image.open("./test/zzh2.bmp")
    martix_gray = np.array(img_gray)[100:110,100:110]
    martix_lsb = np.array(img_lsb)[100:110,100:110]

    #表格绘制，范围为 100-150
    x = range(100,150, 1)
    plt.subplots_adjust(hspace=0.3) # 调整子图间距
    plt.subplot(211)
    plt.title("img_gray")
    plt.hist(martix_gray.flatten(),bins=np.arange(100,150,1),rwidth=0.1,align='left')
    plt.xticks(x)

    plt.subplot(212)
    plt.title("img_lsb")
    plt.hist(martix_lsb.flatten(),bins=np.arange(100,150,1),rwidth=0.1,align='left')
    plt.xticks(x)

    plt.show()

main()

