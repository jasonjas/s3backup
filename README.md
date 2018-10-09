# s3backup
Python 3.7 utility for uploading files to AWS S3

# Requirements
Python 3.7
  - boto3 module

AWS access key / secret key file
  - See https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html for AWS credentials file format

An existing S3 bucket

# Instructions
- Create AWS credentials file 
- Configure BackupFiles.config file
- Run config_parser.py

# Notes
The BackupFiles.config is created/read by the ConfigParser module
  - backup_locations, awsregion, awsbucket, and awscredentials values must be defined (see example file below)

hashes.txt is automatically created,
  This file contains the hashes of all files uploaded now and previously
  Prevents uploading unchanged files each run


# Example BackupFiles.config
[hashfile]

file = C:\backup\hashes.txt

[backup_locations]
documents = C:\Users\user_name\Documents

otherfiles = E:\importantfiles

[awsregion]

region = us-east-1

[awsbucket]

bucket = bucket_name

[awscredential]

file = c:\Users\user_name\.aws\credentials
