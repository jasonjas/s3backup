# parse config file for files/directories to backup
import configparser
import os
from builtins import input, Exception, open
import hashes
import awsupload
from pathlib import Path



currentdir = Path(__file__).parent
configfile = Path(currentdir / 'BackupFiles.config')
# default hashfile location, can be set in configfile (if it exists)
defaulthashfile = Path(currentdir / 'hashfile.txt')
# cp is for hashfile
cp = configparser.ConfigParser(delimiters='=')
# cpcf is for config file
cpcf = configparser.ConfigParser(delimiters='=')
# hashfile section
section = 'hashes'
sub_string = 0
aws = awsupload.AwsUpload()


def main():
    global hashfileloc
    checkconfigfile()
    checkhashfile()
    # get hashfile directory
    # if cpcf.has_option("hashes", "file"):
    #     hashfileloc = cpcf.get("hashes", "file")
    # else:
    #     hashfileloc = hf
    with open(configfile) as cf:
        for f in cpcf.items("backup_locations"):
            print("checking", f[1])
            # for line in cf.read().splitlines():
            # loopdir(f[1])
            preloop(f[1])


def checkhashfile():
    global hf
    try:
        cp.read_file(open(hf))
    except FileNotFoundError:
        cp.add_section(section)
        with open(hf, "w") as cc:
            cp.write(cc)
        cp.read_file(open(hf))


def hashfile(value):
    global hf
    hf = value


def checkconfigfile():
    global hf
    configsections = {'hashfile': 'file',
                      'backup_locations': 'location1',
                      'awsregion': 'region',
                      'awsbucket': 'bucket',
                      'awscredential': 'file'}
    try:
        cpcf.read_file(open(configfile))
    except FileNotFoundError:
        # create blank file
        writeconfigfile(configfile)
    cferror = None
    for i in configsections:
        opt = configsections[i]
        # create sections if they don't exist
        if not cpcf.has_section(i):
            cpcf.add_section(i)
            cpcf.set(i, opt, "")
            writeconfigfile(configfile)
        # verify all section items have a value
        for item in cpcf.items(i):
            if not item[1]:
                if i == "hashfile":
                    cpcf.set(i, configsections[i], str(defaulthashfile))
                    writeconfigfile(configfile)
                else:
                    cferror = i
        # verify all options exist
        if not cpcf.has_option(i, opt):
            if i == "backup_locations":
                # check if any option exists
                if not cpcf.items(i):
                    cferror = i
            else:
                input(i)
                cpcf.set(i, opt, "")
                cferror = i
                writeconfigfile(configfile)
        else:
            if i == "hashfile":
                hf = cpcf.get("hashfile", "file")
            if i == "awsregion":
                aws.region = cpcf.get(i, opt)
            if i == "awsbucket":
                aws.bucket = cpcf.get(i, opt)
            if i == "awscredential":
                aws.credentialfile = cpcf.get(i, opt)
    if cferror:
        raise Exception("Missing %s value in config file" % cferror)


def writeconfigfile(cfgfile):
    # cpcf.read_file((open(cfgfile)))
    with open(cfgfile, "w") as cf:
        cpcf.write(cf)
    cpcf.read_file((open(cfgfile)))


def preloop(item):
    global sub_string
    if os.name == 'nt':
        # sub_string creates the Key parameter used by s3 upload
        sub_string = item.index(item.split('\\')[-1])
    else:
        sub_string = item.index(item.split('/')[-1])
    loopdir(item)


def loopdir(d):
    global hf
    try:
        if os.path.isfile(d):
            h = hashes.get_hash(d)
            ret = hashes.check_hash(d, h, section, hf, cp)
            # return is None for matching files
            if ret:
                print(aws.s3upload(d, sub_string))
                # write new or updated hash
                cp.set(section, d, h)
                with open(hf, "w") as cc:
                    cp.write(cc)
        else:
            for x in os.listdir(d):
                fullx = os.path.join(d, x)
                loopdir(fullx)
    except FileNotFoundError:
        print(d, "is not a valid file or directory")

if __name__ == '__main__':
    main()
