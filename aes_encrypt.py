from Cryptodome.Cipher import AES
# from Cryptodome import Random
from binascii import b2a_hex, a2b_hex
import pickle
from bin.config import Const
import openpyxl


class MyAES:
    """
    AES加密类
    # 将可以pickle的对象加密并写入到文件
    wb = openpyxl.load_workbook('../datafiles/金蝶-K3cloud(Oracle)-财务模块.xlsx')  # workbook对象
    MyAES().save_encrypt_obj(wb, '../datafiles/111.interface')  # 将一个对象变成pickle对象,然后对其加密,存放在path文件
    d_obj = MyAES().load_decrypt_obj('../datafiles/111.interface')  # 读取path文件内容,解密成pickle对象,返回原来的对象
    # 将str或bytes类型加密并输出密文
    ss = '这是一段明文!'
    encrypt_str = MyAES().encrypt(ss)
    print(encrypt_str[0])
    decrypt_str = MyAES().decrypt(encrypt_str[0], encrypt_str[1])
    print(decrypt_str)
    """

    def __init__(self, key=None):
        """
        :param key: 密码,如: key=b'passwordpassword'
        # 长度必须为16位（AES-128）或24位（AES-192）或32位（AES-256）Bytes 长度.目前AES-128足够用
        """
        if not key:
            key = Const.AES_PASSWORD
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt_obj(self, obj):
        """
        将对象加密
        :param obj: 需要加密的可以pickle对象
        :return:
        """
        pkl_obj = pickle.dumps(obj)
        return self.encrypt(pkl_obj)

    def save_encrypt_obj(self, obj, path):
        """
        将对象加密,并写到文件
        :param obj:
        :param path:
        :return:
        """
        txt = self.encrypt_obj(obj)
        with open(path, 'wb') as f:
            f.write(pickle.dumps(txt[0]))

    def encrypt(self, text, encoding='utf8'):
        """
        加密
        :param text: 明文
        :param encoding: 明文字符集:当text_type为str时使用
        :return:
        """
        text_type = type(text)  # 获取明文类型,用于解密时候需不需要将bytes类型转换成str
        text = text if text_type == bytes else bytes(text, encoding=encoding)  # 转换成bytes
        text = self.supplement(text)  # 明文长度需要是16的倍数,这里进行长度补位
        cryptor = AES.new(self.key, self.mode, self.key)
        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext), text_type

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text, text_type=str, encoding='utf8'):
        """
        解密
        :param text: 密文
        :param text_type: 明文类型:str or bytes 默认为:str
        :param encoding: 明文字符集:当text_type为str时使用
        :return:
        """
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))  # 解密出来后是bytes
        if text_type == str:
            plain_text = plain_text.decode(encoding)  # 转换成str
            return plain_text.rstrip('\0')  # 去除补位
        elif text_type == bytes:
            return plain_text.rstrip(b'\x00')  # 去除补位

    @staticmethod
    def supplement(text):
        """
        明文长度需要是16的倍数,这里进行长度补位
        :param text:明文
        :return:
        """
        count = 16 - (len(text) % 16)
        if isinstance(text, str):
            return text + ('\0' * count)
        elif isinstance(text, bytes):
            return text + (b'\x00' * count)
        else:
            return text

    def load_decrypt_obj(self, path):
        """
        将密文还原成对象
        :param path: 需要解密的文件
        :return:
        """
        with open(path, 'rb') as f:
            encrypt_txt = pickle.loads(f.read())
        decrypt_obj = self.decrypt(encrypt_txt, bytes)
        obj = pickle.loads(decrypt_obj)
        return obj
