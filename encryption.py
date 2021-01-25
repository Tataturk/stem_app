from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(f"keys/private.key", 'wb') as f:
        f.write(private_key)

    public_key = key.publickey().export_key()
    with open(f"keys/public.pub", 'wb') as f:
        f.write(public_key)

def encrypt(student,file):
    session_key = get_random_bytes(16)
    with open(f"{student}.id", 'wb') as h:
        h.write(session_key)
    frans_key = RSA.import_key(open("keys/public.pub").read())

    #read file.txt
    with open(file, 'rb') as f:
        data = f.read()
    
    #open output
    file_out = open(f"{student}.code", 'wb')

    #encoded key write to file
    cipher_rsa = PKCS1_OAEP.new(frans_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    with open(f"{student}.skey", 'wb') as g:
        g.write(enc_session_key)

    #encrypt met aes session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
    [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
    file_out.close()

def decrypt(student):
    file_in = open(f"{student}.code", "rb")

    private_key = RSA.import_key(open("keys/private.key").read())

    enc_session_key, nonce, tag, ciphertext = \
    [ file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(data.decode("utf-8"))

#generate_keys()
#encrypt('encryption/stem_app','test.txt')
decrypt('encryption/stem_app')