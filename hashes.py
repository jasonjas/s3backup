# hashes.py
import hashlib


def get_hash(f):
    c = hasher(f)
    return c


def check_hash(file, filehash, section, hashfile, cp):
    # print("%s , %s , %s" % (section, file, filehash))
    if cp.has_option(section, file):
        if filehash in cp.get(section, file):
            return
        else:
            # upload file and update hash
            # cp.set(section, file, filehash)
            # with open(hashfile, "w") as cc:
            #     cp.write(cc)
            return "uploading " + file
    else:
        # cp.set(section, file, filehash)
        # with open(hashfile, "w") as cc:
        #     cp.write(cc)
        return "uploading " + file


def hasher(f):
    # Specify how many bytes of the file you want to open at a time
    BLOCKSIZE = 65536
    FILE = f
    sha = hashlib.sha256()
    with open(FILE, 'rb') as kali_file:
        file_buffer = kali_file.read(BLOCKSIZE)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            file_buffer = kali_file.read(BLOCKSIZE)
    return sha.hexdigest()