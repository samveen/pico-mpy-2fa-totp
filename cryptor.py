import hashlib
import cryptolib

def encrypt(filename,key):
    hasher=hashlib.sha256(key)
    digest=hasher.digest()
    encryptor = cryptolib.aes(digest, 1)
    try:
        with open(filename,"r") as f:
            data=f.read()
            data_bytes = data.encode()
            encdata=encryptor.encrypt(data_bytes + b'\x00' * ((16 - (len(data_bytes) % 16)) % 16))
            with open("{}.encoded".format(filename),"w") as fw:
                return(fw.write(encdata))
    except Exception as e:
        print("Error: cryptor::encrypt:",e)
        return None

def decrypt(filename,key):
    hasher=hashlib.sha256(key)
    digest=hasher.digest()
    try:
        with open(filename,"rb") as f:
            dataread=f.read()
        decryptor = cryptolib.aes(digest, 1)
        return decryptor.decrypt(dataread)
    except Exception as e:
        print("Error: cryptor::decrypt:",e)
        return None


