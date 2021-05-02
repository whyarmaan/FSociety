import hashlib
from Crypto.Cipher import AES
import pickle

def padd_message(message):
	result = message
	while len(result) % 16 != 0:
		result += b" "
	return result		

key = "&6^34={"
hashed_key = hashlib.sha256(key.encode('utf8')).digest()
mode = AES.MODE_CBC
IV = "qw#xbgy6&9)-=%4@"
encrypter = AES.new(hashed_key, mode, IV)

def hash(value):
	return encrypter.encrypt(padd_message(value))
