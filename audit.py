import csv
import io

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, SHA

gSigner = "signer@stem_app"

def loadVoters(fname):
    try:
        voters = { s['studNr']: s for s in csv.DictReader(loadFile(fname), delimiter=';') }
        return voters
    except Exception as e:
        return {}

def loadCandidates(fname):
    try:
        candidates = { s['mdwId']: s for s in csv.DictReader(loadFile(fname), delimiter=';') }
        return candidates
    except Exception as e:
        return {}

def sign(data, signer=gSigner, sfx='.prv'):
    if isinstance(data, io.StringIO): data = data.read()
    if not isinstance(data, bytes): data = bytes(data, encoding='utf-8')

    key = RSA.import_key(open('keys/private.key').read())
    h = SHA256.new(data)
    signature = pkcs1_15.new(key).sign(h)

    return ':'.join(['#sign', 'sha256-PKCS1-rsa2048', signer, signature.hex()])

def verify(data, signature, signer=gSigner, sfx='.pub'):
    if isinstance(data, io.StringIO): data = data.read()
    if not isinstance(data, bytes): data = bytes(data, encoding='utf-8')
    flds = signature.split(':')
    if flds[1] != 'sha256-PKCS1-rsa2048' and flds[2] != signer:
        print('Error: Unknown signature:', signature)
        return None
    sign = bytes.fromhex(flds[3])

    key = RSA.import_key(open('keys/public.pub').read())
    h = SHA256.new(data)
    res = False
    try:
        pkcs1_15.new(key).verify(h, sign)
        print ("The signature is valid.")
        res = True
    except (ValueError, TypeError):
        print("The signature is not valid.")
        res = False
    return res

def saveFile(fname, data, signer=gSigner, useSign=True, ):
    """ Save file check signature """  

    if isinstance(data, io.StringIO): data = data.read()
    n = data.find('#sign')
    if n > 0:
        data = data[0:n]
    if useSign:
        data += sign(data, signer) + '\n'
    io.open(fname, 'w', encoding='UTF-8').write(data)
    return

def loadFile(fname, useSign=True, signer=gSigner):
    """ Load file check signature """  
    data = io.open(fname, 'r', encoding='UTF-8').read()
    n = data.find('#sign')
    if n > 0:
        sign = data[n:].strip()
        data = data[0:n]
        if useSign:
            res = verify(data, sign, signer, sfx='.pub')
            if not res: return None
    return io.StringIO(data)