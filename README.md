# s3backup
Python 3.7 utility for uploading files to AWS S3

# Requirements
Python 3.7
  boto3 module

AWS access key / secret key file

An existing S3 bucket

# Instructions
The BackupFiles.config is created/read by the ConfigParser module

hashes.txt is automatically created,
  This file contains the hashes of all files uploaded now and previously
  Prevents uploading unchanged files each run


# Example BackupFiles.config
[hashfile]
file = C:\backup\hashes.txt

[backup_locations]
documents = C:\Users\user_name\Documents

[awsregion]
region = us-east-1

[awsbucket]
bucket = bucket_name

[awscredential]
file = c:\Users\user
