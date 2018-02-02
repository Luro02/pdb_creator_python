import sys
import os

JP = ['G','C']
US = ['A', 'E']
EU = ['F', 'B']
KO = ['H']

nonpdrmheader = bytes.fromhex('0001000100010002efcdab8967452301')

def checkNoNPDRM(filepath):
    with open(filepath, "rb") as f:
            if f.read(16) != nonpdrmheader:
                if (len(sys.argv) < 2):
                    print("Error", "Not a valid NoNPDRM license.")
                else:
                    print("Error: Not a valid NoNPDRM License.")
                return False
            else:
                return True

def getContentID(filepath):
    with open(filepath, "rb") as f:
        # Get Content ID
        f.seek(16)
        contentid = f.read(36).decode('ascii')
        return contentid

def getTitleID(filepath):
    with open(filepath, "rb") as f:
        # Get Title ID
        f.seek(23)
        titleid = f.read(9).decode('ascii')
        return titleid

def getKey(filepath):
    """
    imports Klicensee from fake license
    """
    with open(filepath, "rb") as f:
        # Get key
        f.seek(80)
        key = f.read(16)
        return key.hex().upper()

def getExtractedKey(filepath):
    """
    I don't know what kind of key this is...
    ask the creator ^^
    """
    with open(filepath, "rb") as f:
        # Get key
        key = f.read(16)
        return key.hex().upper()

def getTitleIDFromContentID(contentid):
    return contentid[7:16]

def getRegion(id):
    if len(id) == 9:
        i = 3
    elif len(id) == 36:
        i = 10
    # Determine region
    if id[i] in JP:
        return "JP"
    elif id[i] in US:
        return "US"
    elif id[i] in EU:
        return "EU"
    elif id[i] in KO:
        return "KO"

def showPKGInfo(contentid, titleid, region, key):
    pkg_info = ("Content ID: {}\nTitle ID: {}\nRegion: {}\nLicense Key: {}".format(contentid, titleid, region, key.hex().upper()))
    if len(sys.argv) < 2:
        print("Info", pkg_info)
    else:
        print(pkg_info)

def saveBinary(key, out_dir, filename):
    # Save filename.bin
    with open(out_dir.joinpath("{}.bin".format(filename)), "wb") as keybin:
        keybin.write(key)

def rebuildLicense(key, out_dir, contentid):
    with open(out_dir.joinpath("6488b73b912a753a492e2714e9b38bc7.rif"), 'wb') as rebuiltlicense:
        rebuiltlicense.write(nonpdrmheader)
        rebuiltlicense.write(contentid)
        rebuiltlicense.seek(80)
        rebuiltlicense.write(key)
        rebuiltlicense.seek(511)
        rebuiltlicense.write(b'\x00')
