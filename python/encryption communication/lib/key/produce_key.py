
#使用 rsa 生成公钥、私钥：
import rsa
import os,sys

#相对路径错误的话，可以改为绝对路径
pem_dir = "../../res/pem/"


f, e = rsa.newkeys(1024)    # 生成公钥、私钥
 
e = e.save_pkcs1()  # 保存为 .pem 格式
with open(pem_dir+'client_private_key.pem', "wb") as x:  # 保存私钥
    x.write(e)
f = f.save_pkcs1()  # 保存为 .pem 格式
with open(pem_dir+'client_public_key.pem', "wb") as x:  # 保存公钥
    x.write(f)


f, e = rsa.newkeys(1024)    # 生成公钥、私钥

e = e.save_pkcs1()  # 保存为 .pem 格式
with open(pem_dir+'serve_private_key.pem', "wb") as x:  # 保存私钥
    x.write(e)

f = f.save_pkcs1()  # 保存为 .pem 格式
with open(pem_dir+'serve_public_key.pem', "wb") as x:  # 保存公钥
    x.write(f)

