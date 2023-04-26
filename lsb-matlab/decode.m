clc %清屏
clear %清空变量
close all %关闭已打开图像

plain_image = imread('Lenna.bmp');
lsb_image = imread('encode_result\1.bmp');
plain_image = rgb2gray(plain_image); 

[height,width,s]=size(plain_image);
secret_image = zeros(height,width,1);
for i=1:height
    for j=1:width
        a=bitget(plain_image(i,j),1);             %提取这个位的值
        b=bitget(lsb_image(i,j),1);
        secret_image(i,j)=bitset(secret_image(i,j),1,b);
    end
end

imshow(secret_image);
imwrite(secret_image,'secret_image.bmp');