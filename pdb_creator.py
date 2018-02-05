#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
import os
import sys
import wget
import getopt
import zrif2rif as z2r
from shutil import copy2

def arguments():
	package = None
	zrif = None

	opts, rest = getopt.getopt(sys.argv[1:], "p:z:")
	for opt, arg in opts:
		if opt == '-p':
			package = arg
		if opt == '-z':
			zrif = arg
	if package == None:
		print("pdb_creator v.1.0.1")
		print("")
		print("Usage:")
		print("	  pdb_creator [-p filename.pkg] [-z ZRIF]")
		print("")
		print("Parameters:")
		print("	  -p			Input Theme PKG")
		print("	  -z			Zrif")
		print("")
		sys.exit("Error: No Input Package specified !")
	if zrif == None:
		print("pdb_creator v.1.0.1")
		print("")
		print("Usage:")
		print("	  pdb_creator [-p filename.pkg] [-z ZRIF]")
		print("")
		print("Parameters:")
		print("	  -p			Input Theme PKG")
		print("	  -z			ZRif")
		print("")
		sys.exit("Error: No ZRif-String specified !")
	return package, zrif

def exists(path):
    """
    Test whether a path exists.
    Returns False if not found.
    """
    try:
        status = os.stat(path)
    except os.error:
        return False
    return True

def leadingzeros(var):
	return f'{var:08}'

def create_theme(package, zrif):
	folder_number = int(1)

	while exists("bgdl/t/{}".format(leadingzeros(folder_number))) == True:
		folder_number += 1
	
	folder_number = str(leadingzeros(folder_number))


	cid = z2r.cid_fetch(package)
	tid = z2r.offsets_read(package, 55, 63)
	z2r.zrif2rif(zrif, "bgdl/t/{}/{}/sce_sys/package/work.bin".format(folder_number, tid.decode("utf-8")))

	if os.path.isfile(sys._MEIPASS + os.sep + 'pkg_dec.exe'):
		z2r.syscmd('{}{}pkg_dec {} bgdl/t/{}/{}/'.format(sys._MEIPASS, os.sep, package, folder_number, tid.decode("utf-8")))
	else:
		z2r.syscmd('pkg_dec {} bgdl/t/{}/{}/'.format(package, folder_number, tid.decode("utf-8")))

	if len(tid) != len("PCSG90218"):
		tid = tid + b'\x00'

	if os.path.isfile(sys._MEIPASS + os.sep + 'assets' + os.sep + 'd0.pdb'):
		# Copy Files:
		copy2(sys._MEIPASS + os.sep + "assets/icon.png", "bgdl/t/{}/icon.png".format(folder_number))
		copy2(sys._MEIPASS + os.sep + "assets/d0.pdb", "bgdl/t/{}/d0.pdb".format(folder_number))
		copy2(sys._MEIPASS + os.sep + "assets/d1.pdb", "bgdl/t/{}/d1.pdb".format(folder_number))
		copy2(sys._MEIPASS + os.sep + "assets/f0.pdb", "bgdl/t/{}/f0.pdb".format(folder_number))
	else:
		# Copy Files:
		copy2("assets/icon.png", "bgdl/t/{}/icon.png".format(folder_number))
		copy2("assets/d0.pdb", "bgdl/t/{}/d0.pdb".format(folder_number))
		copy2("assets/d1.pdb", "bgdl/t/{}/d1.pdb".format(folder_number))
		copy2("assets/f0.pdb", "bgdl/t/{}/f0.pdb".format(folder_number))

	# Write to Files:
	
	z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 634, cid.encode("utf-8")) # CID
	z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 778, tid) # TITLE_ID
	z2r.offsets_write("bgdl/t/{}/d0.pdb".format(folder_number), 852, tid) # TITLE_ID_2


	z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 634, cid.encode("utf-8")) # CID
	z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 778, tid) # TITLE_ID
	z2r.offsets_write("bgdl/t/{}/d1.pdb".format(folder_number), 852, tid) # TITLE_ID_2

if __name__ == "__main__":
	package, zrif = arguments()
	create_theme(package, zrif)
