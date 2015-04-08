#!/usr/bin/env python2
# python recv.py
import snap
import pprint
import requests
import time
import uuid
import sys
import json
import imghdr
import os

pp = pprint.PrettyPrinter()

username="UserNameHere"

#The folder relative to this script to save the images.
folder="snaps/"
path=os.path.dirname(os.path.realpath(__file__))+"/"+folder

timestamp = "UnixTimeStamp"
req_token = "Hex"

base = "https://feelinsonice.appspot.com"

#update
update = requests.post(base + "/bq/updates", data={
	"req_token": req_token,
	"timestamp": timestamp,
	"username": username
}, headers={"User-agent": snap.ua})

#Get snap list
snaps = update.json()["snaps"]

#Download all snaps that are not read
for mysnap in snaps:
	imgid=mysnap["id"]
	sender=mysnap.get('sn', '')

	#ignore null senders (These are stories which I'm not doing right now)
	if sender is "":
		continue
	
	#Only process images
	if mysnap["m"] != snap.IMAGE:
		continue

	#Only process unviewd images
	if mysnap["st"] != snap.DELIVERED:
		continue

	#Only process NEW images
	filename=path + sender + "_" + imgid
	if os.path.isfile(filename + ".jpeg"):
		continue
	elif os.path.isfile(filename + ".jpg"):
		continue
	elif os.path.isfile(filename + ".png"):
		continue
	elif os.path.isfile(filename + ".bmp"):
		continue

	#Retreieve file
	snapfile = requests.post(base + "/ph/blob", data={
		"req_token": req_token,
		"timestamp": timestamp,
		"username": username,
		"id": imgid,
	}, headers={"User-agent": snap.ua})

	snapblob = snapfile.content
	snapblob = snapblob.replace("\r", "").replace("\n", "")

	#Write the Image File
	f = open(filename, 'w')
	f.write(snap.decode_stream(snapfile.content))
	f.close()

	#Determine the image type and rename
	filetype=imghdr.what(filename)
	try:
		filetype
		os.rename(filename, filename + "." + filetype)
	except TypeError:
		#Do jack
		1
