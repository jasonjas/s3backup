import boto3, os

bucket = None
credentialfile = None
region = None


class AwsUpload():
    def __init__(self):
        self.bucket = bucket
        self.credentialfile = credentialfile
        self.region = region
        self.s3 = None

    def setvars(self):
        boto3.setup_default_session(region_name=self.region)
        # uses default credential`
        os.environ["AWS_SHARED_CREDENTIALS_FILE"] = self.credentialfile
        # region and shared credential file must be defined before initiating boto3.resource
        self.s3 = boto3.resource('s3')

    def s3upload(self, item, sub_string=0):
        self.setvars()
        if os.name == 'nt':
            # Change substring to UNIX URI for s3
            ss = item[int(sub_string):].replace('\\', '/')
        else:
            ss = item[int(sub_string):]
        obj = self.s3.Object(self.bucket, item)
        # sets ACL to be private
        # See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.copy_object
        #obj.put(Body=open(item, 'rb'), Bucket=self.bucket, ACL='private', Key=ss)
        return "successfully uploaded: " + ss
