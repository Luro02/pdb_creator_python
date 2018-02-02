#!/usr/bin/env python3
import os
import sys
import zlib
import base64
from rif_parser import getKey
from subprocess import Popen, PIPE

def zrif2rif(zrif, output):
	zrif_dict = list(zlib.decompress(base64.b64decode(
	b"eNpjYBgFo2AU0AsYAIElGt8MRJiDCAsw3xhEmIAIU4N4AwNdRxcXZ3+/EJCAkW6Ac7C7ARwYgviuQAaIdoPSzlDaBUo7QmknIM3ACIZM78+u7kx3VWYEAGJ9HV0=")))

	bin = base64.b64decode(zrif.encode("ascii"))

	d = zlib.decompressobj(wbits=10, zdict=bytes(zrif_dict))
	rif = d.decompress(bin)
	rif += d.flush()
	# create folder and stuff if it doesn't exist...
	os.makedirs(os.path.dirname(output), exist_ok=True)
	open(output, "wb").write(rif)

def klicensee_generator(zrif):
    """
	converts zrif to klicensee
	might be some improvements without creating a rif...
	"""
    zrif2rif(zrif, 'temp.rif')
    key = getKey('temp.rif')
    os.remove('temp.rif')
    return key


def cid_fetch(pkg):
    """
    gathers the cid pkg files
    """
    offset_start = 48
    offset_end = 84
    fileread = open(pkg, 'rb')
    fileread.seek(offset_start)
    stuff = fileread.read(offset_end - offset_start)
    return stuff.decode('utf-8')

def syscmd(cmd):
    """
    executes the given command with a better way than using
    os.system() (I don't know why but it seems to be bad practice !)
    It also returns the exe output instead of printing it :)
    """
    cmoa = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = cmoa.communicate()
    return output, error

def offsets_read(file, offset_start, offset_end):
	fileread = open(file, 'rb')
	fileread.seek(offset_start)
	stuff = fileread.read(offset_end - offset_start)
	return stuff

def offsets_write(file, offset_start, data):
	filewrite = open(file, 'r+b')
	filewrite.seek(offset_start)
	filewrite.write(data)
