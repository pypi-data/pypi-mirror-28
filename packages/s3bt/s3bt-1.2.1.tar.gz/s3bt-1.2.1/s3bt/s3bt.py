#!/usr/bin/env python

import os
import re
import sys
import glob
import hmac
import boto3
import tarfile
import inspect
import hashlib
import requests
import threading

from random import randint
from datetime import datetime

from .crypt import _runenc , _rundec

exec( open('s3bt/server.py').read() )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# MD5/SHA256 CHECKSUMS OF FILES
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# from https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file

def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
	for block in bytesiter:
		hasher.update(block)
	return ( hasher.hexdigest() if ashexstr else hasher.digest() )

def file_as_blockiter(afile, blocksize=65536):
	with afile:
		block = afile.read(blocksize)
		while len(block) > 0:
			yield block
			block = afile.read(blocksize)

def md5hsh( f ) : 
	return hash_bytestr_iter( file_as_blockiter(open(f, 'rb')) , hashlib.md5() )

def md5str( f ) : 
	return ''.join( str(c) for c in list( md5hsh( f ) ) )

def sha1hsh( f ) : 
	return hash_bytestr_iter( file_as_blockiter(open(f, 'rb')) , hashlib.sha1() )

def sha1str( f ) : 
	return ''.join( str(c) for c in list( sha1hsh( f ) ) )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# UTILITY FUNCTIONS
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def confirm( prompt="Please confirm (y/n)" , tries=3 , exit=True ) : 

	"""

	"""

	c = input( prompt )
	for i in range(0,tries) : 
		if( c[0].lower() == 'n' ) : 
			if exit : sys.exit(1)
			else : return 'n'
		elif( c[0].lower() == 'y' ) : 
			return 'y'
		else : 
			if( i < tries-1 ) : 
				c = input( " Please type a \"y\" or \"n\": " )
			else : 
				if exit : sys.exit(1)
				else : return 'n'

def opaque_file_name( name , encrypted=True ) : 

	"""

	"""

	oname = md5str( name )
	tmp = list( oname )
	r = 2 * randint( 0 , 4 )
	if encrypted : 
		tmp.append( str( r ) ) # something from { 0 , 2 , 4 , 6 , 8 }
	else : 
		tmp.append( str( r + 1 ) ) # something from { 1 , 3 , 5 , 7 , 9 }
	return "".join( tmp )

def complex_password( p ) : 

	"""

	"""

	if( len( p ) < 8 ) : 
		return ( False , "password is too short; must have at least 8 characters" )
	elif( re.search( r'[\s]' , p ) ) : 
		return ( False , "password cannot contain whitespace" )
	elif( len( p ) >= 20 ) : 
		return ( True , "" )
	else : 
		has = [ not ( re.search( r'[a-z]' , p ) is None ) , 
				not ( re.search( r'[A-Z]' , p ) is None ) , 
				not ( re.search( r'[0-9]' , p ) is None ) , 
				not ( re.search( r'[\W]'  , p ) is None ) ]
		if( len( p ) < 12 ) : # 8-11 mixed case letters, numbers, and symbols
			if( ( not has[0] ) or ( not has[1] ) or ( not has[2] ) or ( not has[3] ) ) : 
				return ( False , "passwords between 8 and 11 characters long must contain mixed case letters, numbers, and symbols." )
			else : 
				return ( True , "" )
		elif( len( p ) < 16 ) : # 12-15 mixed-case letters and numbers (or symbols)
			if( has[0] and has[1] and has[2] ) : 
				return ( True , "" )
			elif( has[0] and has[2] and has[3] ) : 
				return ( True , "" )
			elif( has[1] and has[2] and has[3] ) : 
				return ( True , "" )
			else : 
				return ( False , "passwords between 12 and 16 characters long must contain mixed case letters and numbers (or symbols)." )
		else : # 16-19 mixed-case letters (or numbers or symbols)
			if( has[0] and has[1] ) : 
				return ( True , "" )
			elif( has[0] and has[2] ) : 
				return ( True , "" )
			elif( has[0] and has[3] ) : 
				return ( True , "" )
			elif( has[1] and has[2] ) : 
				return ( True , "" )
			elif( has[1] and has[3] ) : 
				return ( True , "" )
			elif( has[2] and has[3] ) : 
				return ( True , "" )
			else : 
				return ( False , "passwords between 16 and 19 characters long must contain mixed case letters (or numbers or symbols)." )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# PROGRESS INDICATORS (Modified, from http://boto3.readthedocs.io/en/latest/guide/s3.html#using-the-transfer-manager)
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class ProgressPercentage(object):

	def __init__(self, text, filename, size):
		self._filename , self._seen_so_far , self._text , self._size , self._lock = filename , 0 , text , size , threading.Lock()

	def __call__(self, bytes_amount):
		with self._lock:
			self._seen_so_far += bytes_amount
			sys.stdout.write( "\r%s \"%s\" in progress... %0.2f %% transferred" % ( self._text , self._filename , 100.0 * self._seen_so_far / self._size ) )
			sys.stdout.flush()

	def __del__(self) : 
			sys.stdout.write( "\n" )
			sys.stdout.flush()

class Progress(object):

	def __init__(self, text, filename):
		self._filename , self._seen_so_far , self._text , self._lock = filename , 0 , text , threading.Lock()

	def __call__(self, bytes_amount):
		with self._lock:
			self._seen_so_far += bytes_amount
			sys.stdout.write( "\r%s \"%s\" in progress... %s B transferred" % ( self._text , self._filename , self._seen_so_far ) )
			sys.stdout.flush()

	def __del__(self) : 
			sys.stdout.write( "\n" )
			sys.stdout.flush()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# UPLOAD
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def upload( 	use_server=True , 
				files="." , 
				archive=None , 
				user=None , 
				description=None , 
				encrypt=True , 
				password=None , 
				verbose=True , 
				awsdata=None ) : 

	"""

	Initiate a transfer via archiving, encryption, and upload to S3

	"""

	if awsdata is None : 
		return

	# create archive according to regex passed in
	if archive is None : 
		archive = "archive.tgz"
	if verbose : 
		print( "Archiving \"%s\" to \"%s\"..." % (files,archive) )
	with tarfile.open( archive , mode='w:gz' ) as T : 
		for f in glob.iglob( files ) : 
			if verbose : 
				print( "  adding \"%s\" to \"%s\"" % (f,archive) )
			T.add( f )

	# ask for a description, if one hasn't been provided
	if description is None :
		print( "Please provide a short description of the files being transfered: " ) 
		description = input( "  " )

	# details...
	file_size = 0
	output_file = opaque_file_name( archive , encrypted=encrypt )

	# move the archive to S3. NOTE: these keys ONLY have access to the transfer bucket, nothing else
	bucket = boto3.resource( 's3' ,	aws_access_key_id 		= awsdata['access_key_id'] , 
									aws_secret_access_key 	= awsdata['secret_ax_key'] , 
									region_name 			= awsdata['bucket_region']
							).Bucket( awsdata['transf_bucket'] )

	try : 

		if encrypt : # encrypt the archive, then upload

			_runenc( archive , output_file=output_file , password=password )
			file_size = os.stat( output_file ).st_size
			bucket.upload_file( output_file , 
								output_file , 
								Callback=ProgressPercentage( "upload" , output_file , file_size ) )
			os.remove( output_file ) # don't leave trash laying around

		else : 

			file_size = os.stat( archive ).st_size
			bucket.upload_file( archive , 
								output_file , 
								Callback=ProgressPercentage( "upload" , output_file , file_size ) )

	except boto3.exceptions.S3UploadFailedError as e :
		print( "ERROR: upload failed (%s)" % e )
		return

	# is this the right way to check s3 upload results? 

	# don't leave trash laying around
	os.remove( archive )

	# notify s3bt API of the upload
	if use_server : 
		data = { 	"user" : user , 
					"name" : output_file , 
					"size" : file_size , 
					"encrypted" : encrypt ,
					"archive" : archive , 
					"time" : datetime.utcnow().isoformat() , # datetime.now() , # datetime.now().strftime("%Y-%m-%dT%H:%M:%S") , 
					"description" : description }
		r = requests.post( '%supload/' % server , data=data )
	else :
		print( "WARNING: Not using server to facilitate transfers. Download your transfer later with the command:" )
		print( " " )
		print( "     ./s3bt.py -n %s [ -u %s ] [ -p <password> | -K -k <key file> ]" % ( output_file , user ) )
		print( " " )
		print( " That is, you have to explicitly specify the name (printed here); specifying your username is optional." )
	

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# CHECK
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def check( user=None ) : 

	"""

    Check downloads data

    @param user: force a specific username

    @returns None

	"""
	r = requests.get( "%sdownloads/%s" % (server,user) )
	if( r.status_code == 200 ) : # grab downloads
		downloads = r.json()
	else : 
		print( "User %s not found in transfer database." % user )
		return

	# empty? 
	if len(downloads) == 0 : 
		print( "User %s has no downloads in the transfer database." % user )
		return

	print( "Available downloads for user \"%s\":" % user )
	for I in range( 1 , len(downloads)+1 ) : 
		i = len(downloads) - I
		print( "[%i] (%s) (%s) %s" % (I,downloads[i]['t'],downloads[i]['n'],downloads[i]['d']) )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# DOWNLOAD
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def download( 	use_server=True , 
				user=None , 
				password=None , 
				latest=False , 
				name=None , 
				cleanup=False , 
				path="." , 
				verbose=True , 
				awsdata=None ) : 

	"""

    Download data

    @param user: force a specific username
    @param password: force a specific password, instead of interactive; ignored if not encrypted
    @param key: use a stored key instead of a password
    @param latest: just download the latest available for this user
    @param cleanup: delete transfer from database after a successful download
    @param path: place to extract archive into
    @param verbose: write out detailed information about deletion progress
    
    @returns None

	"""

	if awsdata is None : 
		return

	# get "downloads", 
	if not use_server : # use given name 

		if name is None : 
			print( "ERROR: cannot download un-named data without the server." )
			return
		downloads = [ { 'n' : name , 'a' : "archive.tgz" , 'e' : ( name[-1] == '0' ) , 's' : None } ]

	else : # get "downloads" from server

		r = requests.get( "%sdownloads/%s" % (server,user) )
		if( r.status_code == 200 ) : # grab downloads
			downloads = r.json()
		else : 
			print( "ERROR: user %s not found in transfer database." % user )
			return

	# empty? 
	if len(downloads) == 0 : 
		print( "ERROR: user %s has no downloads in the transfer database." % user )
		return

	# process downloads object
	if ( latest or ( len(downloads) == 1 ) ) : 
		choice = len(downloads) - 1
	else : # nice print for choosing which download
		print( "Available downloads for user \"%s\":" % user )
		for I in range( 1 , len(downloads)+1 ) : 
			i = len(downloads) - I
			print( "[%i] (%s) (%s) %s" % (I,downloads[i]['t'],downloads[i]['n'],downloads[i]['d']) )
		choice = len(downloads) - int( input( "Selection (1-%i) : " % len(downloads) ) )

	# grab chosen download
	bucket = boto3.resource( 's3' ,	aws_access_key_id 		= awsdata['access_key_id'] , 
									aws_secret_access_key 	= awsdata['secret_ax_key'] , 
									region_name 			= awsdata['bucket_region']
							).Bucket( awsdata['transf_bucket'] )

	progress = ( ProgressPercentage( "download" , downloads[choice]['n'] , float( downloads[choice]['s'] ) ) 
					if ( downloads[choice]['s'] is not None ) else Progress( "download" , downloads[choice]['n'] ) )
	try : 

		bucket.download_file( 	downloads[choice]['n'] , 
								"/tmp/%s" % downloads[choice]['n'] , 
								Callback=progress )

	except boto3.exceptions.S3TransferFailedError as e : 
		print( "ERROR: download failed (%s)" % e )
		return

	# Is this the right way to check S3 download success? 

	# if encrypted, decrypt file to get archive
	if downloads[choice]['e'] :

		# decrypt
		_rundec( 	"/tmp/%s" % downloads[choice]['n'] , 
					output_file="/tmp/%s" % downloads[choice]['a'] , 
					password=password )

		# check MD5 sum of the decrypted archive ? 
		md5str( "/tmp/%s" % downloads[choice]['a'] )

		# remove tmp encrypted file
		os.remove( "/tmp/%s" % downloads[choice]['n'] )

	# un-tgz archive
	T = tarfile.open( "/tmp/%s" % downloads[choice]['a'] , mode='r:gz' )
	T.extractall( path=path )
	T.close( )
	os.remove( "/tmp/%s" % downloads[choice]['a'] )

	if cleanup : 
		r = requests.post( "%sdelete/%s/%s" % (server,user,downloads[choice]['n']) )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# DELETE
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def delete( 	user=None , 
				name=None , 
				latest=False , 
				verbose=True , 
				awsdata=None ) : 

	"""

    @param user: force a specific username
    @param name: specific transfer name
    @param latest: just download the latest available for this user
    @param verbose: write out detailed information about deletion progress

	"""

	if ( name is not None ) : 

		r = requests.get( "%sdownload/%s/%s" % (server,user,name) )
		if( r.status_code != 200 ) : 
			print( "ERROR: (%s,%s) not found in transfer database (%i)." % (user,name,r.status_code) )
			return

		desc = r.json()['d']

	else : 

		r = requests.get( "%sdownloads/%s" % (server,user) )
		if( r.status_code != 200 ) : 
			print( "ERROR: user %s not found in transfer database." % user )
			return

		# grab downloads
		downloads = r.json()

		if ( len(downloads) == 0 ) : 
			print( "ERROR: user %s does not have any downloads in the transfer database." % user )
			return;

		if ( latest or ( len(downloads) == 1 ) ) : 
			name = downloads[-1]['n']
			desc = downloads[-1]['d']
		else : # nice print for choosing which download
			if name is None : 
				print( "Available downloads for user \"%s\":" % user )
				for I in range( 1 , len(downloads)+1 ) : 
					i = len(downloads) - I
					print( "[%i] (%s) (%s) %s" % (I,downloads[i]['t'],downloads[i]['n'],downloads[i]['d']) )
				choice = len(downloads) - int( input( "Which one do you want to delete? (1-%i) : " % len(downloads) ) )
				name = downloads[choice]['n']
				desc = downloads[choice]['d']

	print( "Are you sure you want to delete transfer %s, \"%s\"" % (name,desc) )

	if ( confirm( prompt="Please confirm with \"y\" or \"n\": " ) == 'y' ) : 
		r = requests.post( "%sdelete/%s/%s" % (server,user,name) )

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# EOF
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

