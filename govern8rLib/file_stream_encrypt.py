from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt_file(in_file_name, out_file_name, password, key_length=32):
    with open(in_file_name, 'rb') as in_file, open(out_file_name, 'wb') as out_file:
        encrypt(in_file, out_file, password)

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))


def decrypt_file(in_file_name, out_file_name, password, key_length=32):
    with open(in_file_name, 'rb') as in_file, open(out_file_name, 'wb') as out_file:
        decrypt(in_file, out_file, password)


def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)




def test_encryption() :
    zipfilename = "/Users/raju/Downloads/jdk-8u65-macosx-x64.dmg"
    newzipfilename = "/Users/raju/Downloads/newjdk-8u65-macosx-x64.dmg"
    outfilename = "/Users/raju/Downloads/encrypt-8u65-macosx-x64.dmg"
    with open(zipfilename, 'rb') as in_file, open(outfilename, 'wb') as out_file:
        encrypt(in_file, out_file, "TestStreamEncrypt")

    with open(outfilename, 'rb') as in_file, open(newzipfilename, 'wb') as out_file:
        decrypt(in_file, out_file, "TestStreamEncrypt")