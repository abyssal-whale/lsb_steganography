# -*- coding: UTF-8 -*-
from PIL import Image
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

input_secret_text_path = "./test/input_secret_text.txt"
raw_img_path = "./test/zzh.bmp"
mod_img_path = "./test/zzh2.bmp"
eof_str = "00000000"
eof = chr(int(eof_str, 2))

def get_text_from_file():
    file = open(input_secret_text_path, "r")
    text = file.read()
    file.close()
    return text

def get_gray_img():
    raw_img = Image.open(raw_img_path)
    if raw_img.mode != "L":
        raw_img = raw_img.convert("L")
    return raw_img

# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

# 加密函数
def encrypt(text):
    key = '9999999999999999'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'aaaaaaaaaaaaaaaa'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)

# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = '9999999999999999'.encode('utf-8')
    iv = b'aaaaaaaaaaaaaaaa'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')

def generate_gap(seed, length):
    gap = []
    seed = max(256, pow(2, seed % 20))
    for i in range(3, length + 3):
        tmp = seed % i
        if tmp == 0:
            tmp = 2
        gap.append(tmp)
    return gap

"""
将秘密信息嵌入到载体图像中
首先将秘密信息转换成二进制字符串，如"a" -> "0110 0001"
在二进制字符串的末尾添加两个0x0000的ASCII码作为结束标志
"""
def insert_text_to_image(text, raw_img, mode:int):
    mod_img = raw_img.copy()
    width = mod_img.size[0]
    height = mod_img.size[1]
    binstr = text2binarystring(text)
    binstr += eof_str + eof_str
    # print(len(binstr))
    i = 0
    seed = mod_img.getpixel((width - 2, height - 2))
    gap = generate_gap(seed, width)
    if mode == 1:   # 非连续替换lsb
        tmp = 0
        for index in range(0, len(binstr)):
            tmp = tmp + gap[index]
            tmp_h = tmp % height
            tmp_w = int(tmp / height)
            value = mod_img.getpixel((tmp_w,tmp_h))
            value = mod_lsb(value, binstr[i])
            mod_img.putpixel((tmp_w,tmp_h), value)
            i = i + 1
    elif mode == 0:   # 连续替换lsb
        for w in range(width):
            for h in range(height):
                if i == len(binstr):
                    break
                value = mod_img.getpixel((w,h))
                value = mod_lsb(value, binstr[i])
                mod_img.putpixel((w,h), value)
                i = i + 1
    else:
        print("please select mode as 0 or 1")
    return mod_img

"""
将value的最低位替换成bit,返回修改后的value
"""
def mod_lsb(value, bit):
    str = bin(value).replace('0b', '').zfill(8)
    lsb = str[len(str)-1]
    if lsb != bit :
        str = str[0:len(str)-1] + bit
    return int(str, 2)

"""
将秘密信息转换成二进制串
先将字符转换成对应的ASCII码，然后转二进制，最后8位对齐，不足的前面用0填充
"""
def text2binarystring(text):
    enctext = str(encrypt(text))
    binstr = ""
    for ch in enctext :
        # ord(ch): 将ch转换成十进制数 bin():转换成0b开头的二进制字符串 zfill:返回指定长度字符串，不足的前面填充0
        binstr += bin(ord(ch)).replace('0b', '').zfill(8)
    return str(binstr)

"""
从图像中提取秘密信息，返回string类型的秘密信息
"""
def get_text_from_image(mod_img, mode:int):
    width = mod_img.size[0]
    height = mod_img.size[1]
    bytestr = ""
    text = ""
    countEOF = 0
    if mode == 0:
        for w in range(width):
            for h in range(height):
                value = mod_img.getpixel((w,h))
                bytestr += get_lsb(value)
                if len(bytestr) == 8 :
                    # 转换成ASCII码
                    # 例："0110 0001" -> 97 -> 'a'
                    ch = chr(int(bytestr, 2))
                    if ch == eof :
                        countEOF = countEOF + 1
                    if countEOF == 2 :
                            break
                    text += ch
                    bytestr = ""
    elif mode == 1:
        seed = mod_img.getpixel((width - 2, height - 2))
        gap = generate_gap(seed, width)
        bytestr = ""
        text = ""
        i = 0
        tmp = 0
        while True:
            tmp = tmp + gap[i]
            tmp_h = tmp % height
            tmp_w = int(tmp / height)
            value = mod_img.getpixel((tmp_w,tmp_h))
            bytestr += get_lsb(value)
            if len(bytestr) == 8:
                # 转换成ASCII码
                # 例："0110 0001" -> 97 -> 'a'
                ch = chr(int(bytestr, 2))
                if ch == eof :
                    countEOF = countEOF + 1
                if countEOF == 2 :
                        break
                text += ch
                bytestr = ""
            i = i + 1
    else:
        print("please select mode as 0 or 1")
    return text

"""
返回像素值的lsb
"""
def get_lsb(value):
    str = bin(value).replace('0b', '').zfill(8)
    lsb = str[len(str)-1]
    return lsb

def main():
    mode = int(input("please choose a mode from 0 and 1, representing successive lsb or not: "))
    text = get_text_from_file()
    raw_img = get_gray_img()
    mod_img = insert_text_to_image(text, raw_img, mode)
    mod_img.save(mod_img_path)
    hidden_text = get_text_from_image(mod_img, mode)
    hidden_text = hidden_text[2:]
    hidden_text = hidden_text[:-2]
    print("plain text is: "+decrypt(bytes(hidden_text,encoding='utf-8')))

if __name__ == '__main__':
    main()