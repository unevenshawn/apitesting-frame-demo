import base64
import hashlib

import rsa as rsa

from api import fileUtil
from api.logUtil import info_log


def MD5(content: str):
    bstr = content.encode("utf-8")
    md5str = hashlib.md5(bstr).hexdigest()
    return md5str.upper()


def b64encrypt(content: str):
    return MD5(b64encode(content).upper())


def b64encode(content: str):
    bstr = content.encode("utf-8")
    b64str = base64.b64encode(bstr).decode("utf-8")
    return b64str


def b64decode(confid: str):
    b64str = confid.encode("utf-8")
    return base64.b64decode(b64str).decode("utf-8")


# 生成公钥和私钥
def gen_key(directory: str):
    pbk_writer = fileUtil.openFileWriter(fileUtil.join(directory, "public.pem"))
    prk_writer = fileUtil.openFileWriter(fileUtil.join(directory, "private.pem"))
    (pub_key, pri_key) = rsa.newkeys(1024)

    pub_key_string = pub_key.save_pkcs1().decode("utf-8")
    info_log(pub_key_string)

    private_key_string = pri_key.save_pkcs1().decode("utf-8")
    info_log(private_key_string)

    pbk_writer.write(pub_key_string)
    prk_writer.write(private_key_string)
    fileUtil.close(pbk_writer, prk_writer)


# 通过公钥加密
def pbk_encrypt(filepath, content: str):
    reader = fileUtil.openFileReader(filepath)
    raw = reader.read().encode("utf-8")
    pub_key = rsa.PublicKey.load_pkcs1(raw)

    bstring = rsa.encrypt(content.encode("utf-8"), pub_key)
    confid = base64.b64encode(bstring).decode("utf-8")
    reader.close()
    return confid


# 通过私钥解密
def prk_decrypt(filepath, confid: str):
    reader = fileUtil.openFileReader(filepath)
    raw = reader.read().encode("utf-8")
    prk_key = rsa.PrivateKey.load_pkcs1(raw)

    rsa_bstr = base64.b64decode(confid.encode("utf-8"))
    content = rsa.decrypt(rsa_bstr, prk_key).decode("utf-8")
    reader.close()
    return content


def sign():
    """
    接口签名的方法还没有完善
    接口签名的一种算法可以是：
    1.将所有的参数，包含url路径中的access_token=XXX这种，param，data或json中的请求参数，全部转换成为key=value的形式
    2.获取当前的timestamp，randomInt等等，加入到k=v中去
    3.将所有的k=v，包括时间戳和随机数的，以key为准，将key做排序，把所有的key=value拼接得到一个string
    4.string通过base64转码，得到一个可以通过web传输的字符串，再用md5进行加密，得到签名
    5.将签名放在请求头中，随请求一并发送
    """

    pass
