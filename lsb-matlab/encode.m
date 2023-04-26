clc %清屏
clear %清空变量
close all %关闭已打开图像

plain_image = imread('Lenna.bmp');                %得到图像
secret_image = imread('woman.bmp');
plain_image = rgb2gray(plain_image);              %若图像是彩色，先要转化为灰度图像
image1=plain_image;
[height,width,s]=size(image1);                             %获取图像大小
subplot(3,3,1)
imshow(plain_image);
for n=1:8
    for i=1:height
        for j=1:width
            % a=bitget(plain_image(i,j),n);             %提取这个位的值
            b=bitget(secret_image(i,j),n);
            image1(i,j)=bitset(image1(i,j),n,b);
        end
    end
    sub = int2str(n);
    path = ['encode_result/',sub,'.bmp'];
    imwrite(image1,path);
    subplot(3,3,n+1)                           %循环显示
    imshow(image1)
    image1=plain_image;
end


