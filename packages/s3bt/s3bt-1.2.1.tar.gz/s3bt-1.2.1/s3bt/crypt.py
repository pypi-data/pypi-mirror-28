
import os
import re
import sys
import base64
import hashlib
from getpass import getpass
from Crypto.Cipher import AES

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# ENCRYPTION/DECRYPTION (from Joe Linoff, https://gist.github.com/jlinoff/412752f1ecb6b27762539c0f6b6d667b)
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

'''
Implement openssl compatible AES-256 CBC mode encryption/decryption.
This module provides encrypt() and decrypt() functions that are compatible
with the openssl algorithms.
This is basically a python encoding of my C++ work on the Cipher class
using the Crypto.Cipher.AES class.
URL: http://projects.joelinoff.com/cipher-1.1/doxydocs/html/
'''

# LICENSE
#
# MIT Open Source
#
# Copyright (c) 2014 Joe Linoff
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ================================================================
# debug
# ================================================================
def _debug(msg, lev=1):

	'''
	Print a debug message with some context.
	'''

	sys.stderr.write('DEBUG:{} ofp {}\n'.format(inspect.stack()[lev][2], msg))


# ================================================================
# get_key_and_iv
# ================================================================
def get_key_and_iv(password, salt, klen=32, ilen=16, msgdgst='md5'):

	'''
	Derive the key and the IV from the given password and salt.
	This is a niftier implementation than my direct transliteration of
	the C++ code although I modified to support different digests.
	CITATION: http://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python
	@param password  The password to use as the seed.
	@param salt	  The salt.
	@param klen	  The key length.
	@param ilen	  The initialization vector length.
	@param msgdgst   The message digest algorithm to use.
	'''

	# equivalent to:
	#   from hashlib import <mdi> as mdf
	#   from hashlib import md5 as mdf
	#   from hashlib import sha512 as mdf
	mdf = getattr(__import__('hashlib', fromlist=[msgdgst]), msgdgst)
	password = password.encode('ascii', 'ignore')  # convert to ASCII

	try:
		maxlen = klen + ilen
		keyiv = mdf(password + salt).digest()
		tmp = [keyiv]
		while len(tmp) < maxlen:
			tmp.append( mdf(tmp[-1] + password + salt).digest() )
			keyiv += tmp[-1]  # append the last byte
		key = keyiv[:klen]
		iv = keyiv[klen:klen+ilen]
		return key, iv
	except UnicodeDecodeError:
		return None, None


# ================================================================
# encrypt
# ================================================================
def encrypt(password, plaintext, chunkit=True, msgdgst='md5'):

	'''
	Encrypt the plaintext using the password using an openssl
	compatible encryption algorithm. It is the same as creating a file
	with plaintext contents and running openssl like this:
	$ cat plaintext
	<plaintext>
	$ openssl enc -e -aes-256-cbc -base64 -salt \\
		-pass pass:<password> -n plaintext
	@param password  The password.
	@param plaintext The plaintext to encrypt.
	@param chunkit   Flag that tells encrypt to split the ciphertext
					 into 64 character (MIME encoded) lines.
					 This does not affect the decrypt operation.
	@param msgdgst   The message digest algorithm.
	'''

	salt = os.urandom(8)
	key, iv = get_key_and_iv(password, salt, msgdgst=msgdgst)
	if key is None:
		return None

	# PKCS#7 padding
	padding_len = 16 - (len(plaintext) % 16)
	if isinstance(plaintext, str):
		padded_plaintext = plaintext + (chr(padding_len) * padding_len)
	else: # assume bytes
		
		padded_plaintext = plaintext + (bytearray([padding_len] * padding_len))

	# Encrypt
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(padded_plaintext)

	# Make openssl compatible.
	# I first discovered this when I wrote the C++ Cipher class.
	# CITATION: http://projects.joelinoff.com/cipher-1.1/doxydocs/html/
	openssl_ciphertext = b'Salted__' + salt + ciphertext
	b64 = base64.b64encode(openssl_ciphertext)
	if not chunkit:
		return b64

	LINELEN = 64
	chunk = lambda s: b'\n'.join(s[i:min(i+LINELEN, len(s))]
								for i in range(0, len(s), LINELEN))
	return chunk(b64)


# ================================================================
# decrypt
# ================================================================
def decrypt(password, ciphertext, msgdgst='md5'):

	'''
	Decrypt the ciphertext using the password using an openssl
	compatible decryption algorithm. It is the same as creating a file
	with ciphertext contents and running openssl like this:
	$ cat ciphertext
	# ENCRYPTED
	<ciphertext>
	$ egrep -v '^#|^$' | \\
		openssl enc -d -aes-256-cbc -base64 -salt -pass pass:<password> -in ciphertext
	@param password   The password.
	@param ciphertext The ciphertext to decrypt.
	@param msgdgst	The message digest algorithm.
	@returns the decrypted data.
	'''

	# unfilter -- ignore blank lines and comments
	if isinstance(ciphertext, str):
		filtered = ''
		nl = '\n'
		re1 = r'^\s*$'
		re2 = r'^\s*#'
	else:
		filtered = b''
		nl = b'\n'
		re1 = b'^\\s*$'
		re2 = b'^\\s*#'

	for line in ciphertext.split(nl):
		line = line.strip()
		if re.search(re1,line) or re.search(re2, line):
			continue
		filtered += line + nl

	# Base64 decode
	raw = base64.b64decode(filtered)
	assert(raw[:8] == b'Salted__' )
	salt = raw[8:16]  # get the salt

	# Now create the key and iv.
	key, iv = get_key_and_iv(password, salt, msgdgst=msgdgst)
	if key is None:
		return None

	# The original ciphertext
	ciphertext = raw[16:]

	# Decrypt
	cipher = AES.new(key, AES.MODE_CBC, iv)
	padded_plaintext = cipher.decrypt(ciphertext)

	if isinstance(padded_plaintext, str):
		padding_len = ord(padded_plaintext[-1])
	else:
		padding_len = padded_plaintext[-1]
	plaintext = padded_plaintext[:-padding_len]
	return plaintext


# include the code above ...
# ================================================================
# _open_ios
# ================================================================
def _open_ios( input_file , output_file ):

	'''
	Open the IO files.
	'''

	ifp = sys.stdin
	ofp = sys.stdout

	if  input_file is not None:
		try:
			ifp = open( input_file , 'rb' )
		except IOError:
			print('ERROR: cannot read file: \"%s\"' % input_file )
			sys.exit(1)

	if  output_file is not None:
		try:
			ofp = open( output_file , 'wb' )
		except IOError:
			print('ERROR: cannot write file \"%s\"' % output_file )
			sys.exit(1)

	return ifp , ofp


# ================================================================
# _close_ios
# ================================================================
def _close_ios( ifp , ofp ):

	'''
	Close the IO files if necessary.
	'''

	if ifp != sys.stdin:
		ifp.close()

	if ofp != sys.stdout:
		ofp.close()


# ================================================================
# _write
# ================================================================
def _write(ofp, out, newline=False):

	'''
	Write out the data in the correct format.
	'''

	if ofp == sys.stdout and isinstance(out, bytes):
		out = out.decode('utf-8', 'ignored')
		ofp.write(out)
		if newline:
			ofp.write('\n')
	elif isinstance(out, str):
		ofp.write(out)
		if newline:
			ofp.write('\n')
	else:  # assume bytes
		ofp.write(out)
		if newline:
			ofp.write(b'\n')


# ================================================================
# _write
# ================================================================
def _read(ifp):

	'''
	Read the data in the correct format.
	'''

	return ifp.read()


# ================================================================
# _runenc
# ================================================================
def _runenc( input_file , output_file=None , password=None , msgdgst="sha1" ) :

	'''
	Encrypt data.
	'''

	if password is None:

		c = 0
		while True:
			password = getpass('Password: ')
			res = complex_password( password ) 
			if( not res[0] ) : 
				print( 'ERROR: %s' % res[1] )
			c = c + 1
			if( c >= 3 ) : 
				raise PasswordError( "too many retries" )

		c = 0
		while True : 
			tmp = getpass('Re-enter Password: ')
			if password == tmp :
				break
			print('')
			print('ERROR: Passwords do not match, please try again.')
			c = c + 1
			if( c >= 3 ) : 
				raise PasswordError( "too many retries" )

	password = hashlib.sha224( password.encode('utf-8') ).hexdigest()

	ifp , ofp = _open_ios( input_file , output_file )
	text = _read( ifp )
	out = encrypt( password , text , msgdgst=msgdgst )
	_write( ofp , out , True )
	_close_ios( ifp , ofp )


# ================================================================
# _rundec
# ================================================================
def _rundec( input_file , output_file=None , password=None , msgdgst="sha1" ) :

	'''
	Decrypt data.
	'''
	
	if password is None:
		password = getpass('Password: ')
		res = complex_password( password ) 
		if( not res[0] ) : 
			raise PasswordError( res[1] )

	password = hashlib.sha224( password.encode('utf-8') ).hexdigest()

	ifp , ofp = _open_ios( input_file , output_file )
	text = _read( ifp )
	out = decrypt( password , text , msgdgst=msgdgst )
	_write( ofp , out , False )
	_close_ios( ifp , ofp )

