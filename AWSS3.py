# AWS S3 Python Client.
# Used for: 
# 	Connecting to AWS S3 with passed-in AWS S3 credentials.
# 	Uploading to AWS S3 with specified local file path and S3 destination path.
#	Downloading from AWS S3 with specified S3 file path and local destination.
# Notes:
# 	Pretend that "self" in functions such as foo(self, arg0, arg1) doesn't
#	exist, meaning when calling a function, don't put anything for "self".
#	i.e: object.foo(arg0, arg1) instead of object.foo(someArg, arg0, arg1).

# AWS Python API.
import boto3
import botocore

class AWSS3(object):
	# AWS Client object that maintains connection to AWS S3 as long as
	# AWSS3 class instance exists.
	awsClient = None
	bucketName = None

	# Initializing by attempting to connect to AWS S3 with passed in credentials.
	# All of the arguments should be string types.
	def __init__(self, awsAccessKeyId, awsSecretAccessKey, bucketName):
		self.awsClient = boto3.client("s3", aws_access_key_id=awsAccessKeyId, aws_secret_access_key=awsSecretAccessKey)
		self.bucketName = bucketName

	def downloadDataFromS3(self, fileName, filePathInS3):
		self.awsClient.download_file(self.bucketName, "userData/" + rawVideoName, rawVideoPath + "/" + rawVideoName)


	def downloadParameterDataFromS3(self, parameterDataName, parameterDataPath):
		self.awsClient.download_file(self.bucketName, "userData/" + parameterDataName, parameterDataPath + "/" + parameterDataName)



awss3Object = AWSS3("AKIAIXW57FAC5P2E3ILA", "io5rMGhuv97FJPKrMtQZFlEnoJDrziz+nN4JsjlU", "vsp-userfiles-mobilehub-602139379")
awss3Object.test()

