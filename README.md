# Object-encryption-by-AES
使用AES为对象加密
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
