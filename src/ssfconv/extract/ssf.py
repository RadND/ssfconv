from Crypto.Cipher import AES
import zlib, struct, os
import zipfile

# 这部分最早可以追溯到 https://github.com/KDE/kimtoy/blob/master/kssf.cpp

def extract_ssf(file_path, dest_dir):
    """
        解压ssf文件到指定文件夹，文件夹不存在会自动创建
        ssf 文件格式目前有两种，一种是加密过后，一种未加密的zip
    """
    def __decrypt(bin):
        # AES 解密内容
        aesKey = b'\x52\x36\x46\x1A\xD3\x85\x03\x66' + \
                b'\x90\x45\x16\x28\x79\x03\x36\x23' + \
                b'\xDD\xBE\x6F\x03\xFF\x04\xE3\xCA' + \
                b'\xD5\x7F\xFC\xA3\x50\xE4\x9E\xD9'
        iv = b'\xE0\x7A\xAD\x35\xE0\x90\xAA\x03' + \
            b'\x8A\x51\xFD\x05\xDF\x8C\x5D\x0F'
        ssfAES = AES.new(aesKey, AES.MODE_CBC, iv)
        plain_bin = ssfAES.decrypt(bin[8:])

        # zlib 解压内容
        data = zlib.decompress(plain_bin[4:]) # 注意要跳过头四字节

        def readUint(offset):
            return struct.unpack('I', data[offset:offset+4])[0]

        # 整个内容的大小
        size = readUint(0)

        # 得到若干个偏移量
        offsets_size = readUint(4)
        offsets = struct.unpack('I'*(offsets_size//4),data[8:8+offsets_size])

        for offset in offsets:
            # 得到文件名
            name_len = readUint(offset)
            filename = data[offset+4:offset+4+name_len].decode('utf-16')
            # 得到文件内容
            content_len = readUint(offset+4+name_len)
            content = data[offset+8+name_len:offset+8+name_len+content_len]
            # 写入文件
            open(dest_dir.rstrip(os.sep)+os.sep+filename, 'wb').write(content)

        return
    
    ssf_bin = open(file_path, 'rb').read()

    if ssf_bin[:4] == b'Skin': # 通过头四字节判断是否被加密
        __decrypt(ssf_bin)
    else:
        # 直接 zip 解压
        with zipfile.ZipFile(file_path) as zf:
            zf.extractall(dest_dir)