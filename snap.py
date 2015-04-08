#!/usr/bin/env python2
import hashlib

saved_auth_file = "snap_auth.dat"

static_token = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9" #Used to create a req_token to log in to an account.

ENCRYPT_KEY_2 = "M02cnQ51Ji97vwT4" #Used to encrypt/decrypt standard snap data (using AES/ECB)

req_token_pattern = "0001110111101110001111010101111011010001001110011000110001000110"

#Used to create a valid req_token. `0` means $hash1, `1` means $hash2.
#Where: $hash1 = sha256(secret + auth_token) and
#       $hash2 = sha256(timestamp + secret)

req_token_secret = "iEk21fuwZApXlz93750dmW22pw389dPwOk" #Used to salt the hashes used in generating req_tokens.

#- various media types:
IMAGE = 0
VIDEO = 1
VIDEO_NOAUDIO = 2
FRIEND_REQUEST = 3
FRIEND_REQUEST_IMAGE = 4
FRIEND_REQUEST_VIDEO = 5
FRIEND_REQUEST_VIDEO_NOAUDIO = 6

#- various media states:
NONE = -1
SENT = 0
DELIVERED = 1
VIEWED = 2
SCREENSHOT = 3

#- Snapchat's User-agent:
ua = "Snapchat/4.1.01 (Nexus 4; Android 18; gzip)"

def request_token(auth_token, timestamp):
    first = hashlib.sha256(req_token_secret + auth_token).hexdigest()
    second = hashlib.sha256(str(timestamp) + req_token_secret).hexdigest()
    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(req_token_pattern)]
    return "".join(bits)


from Crypto.Cipher import AES
import base64
import os

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]
cipher = AES.new(ENCRYPT_KEY_2, AES.MODE_ECB)

def saved_auth(newauth=''):
	#Writing New #No parameter passed, just read.
	if newauth is '':

		try:
			with open(saved_auth_file):
				f = open(saved_auth_file, 'r')
				return f.readline()

		except IOError:
			return ''

	#Parameter used, save it
	else:
		s = open(saved_auth_file, 'w')
		s.write(newauth)
		s.close()

		return newauth

def encode_stream(inputtext):
	encoded = cipher.encrypt(pad(inputtext))
	return encoded

def decode_stream(inputtext):
	decoded = unpad(cipher.decrypt(pad(inputtext)))
	return decoded

from StringIO import StringIO
import gzip

def gz_stream(inputstream):
	zipped = StringIO()
	gz = gzip.GzipFile(fileobj=zipped, mode="w")
	gz.write(inputstream)
	gz.close()
	return zipped.getvalue()
