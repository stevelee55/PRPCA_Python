# AWS S3 Python Client.
# Written by Steve Lee
#
# Used for: 
# 	Connecting to AWS S3 with passed-in AWS S3 credentials.
# 	Uploading to AWS S3 with specified local file path and S3 destination path.
#	Downloading from AWS S3 with specified S3 file path and local destination.
#
# Notes:
# 	Pretend that "self" in functions such as foo(self, arg0, arg1) doesn't
#		exist, meaning when calling a function, don't put anything for "self".
#	i.e: object.foo(arg0, arg1) instead of object.foo(someArg, arg0, arg1).
#
# Things to keep in mind:
# 	S3 does not have the concept of "directories", but instead uses the concept of "keys". This means that an object can
# 		be set at a location even if the location doesn't exist.
# 	Use the designated key in S3 called "derek/(content you desire)" when uploading files or donwloading files from.
#
#### DO NOT SHARE THE BELOW CONTENTS FOR SECURITY REASONS!!! ####
#
# AWS Access Keys and bucket name:
# 	AWS Access Key ID: AKIAIXW57FAC5P2E3ILA
#	AWS Secret Access Key: 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
#	Bucket Name: vsp-userfiles-mobilehub-602139379


# AWS Python API.
import boto3
import botocore 

class AWSS3(object):
	# AWS Client object that maintains connection to AWS S3 as long as
	# AWSS3 class instance exists.
	awsClient = None
	# S3 bucket that is used for data/file storage.
	bucketName = None

	# Initializing by attempting to connect to AWS S3 with passed in credentials.
	# All of the arguments should be string types.
	def __init__(self, awsAccessKeyId, awsSecretAccessKey, bucketName):
		self.awsClient = boto3.client("s3", aws_access_key_id=awsAccessKeyId, aws_secret_access_key=awsSecretAccessKey)
		self.bucketName = bucketName

	# "dataPath" is defined by: "derek/content", no "/" or "./" in the beginning, with no "/" at the end.
	# "dataDestination" is defined by: "./dir0/dir1/content", "/" or "./" in the beginning, with no "/" at the end.
	def downloadDataFromS3(self, dataPath, dataDestinationPath):
		self.awsClient.download_file(self.bucketName, dataPath, dataDestinationPath)

	# "dataPath" is defined by: "./dir0/dir1/content", "/" or "./" in the beginning, with no "/" at the end.
	# "dataDestination" is defined by: "derek/content", no "/" or "./" in the beginning, with no "/" at the end.
	def uploadDataToS3(self, dataPath, dataDestinationPath):
		self.awsClient.upload_file(dataPath, self.bucketName, dataDestinationPath)

###################################################################
# Comment below out when using the class above.

# Sample Code.
# Initializing.
awss3Object = AWSS3("AKIAIXW57FAC5P2E3ILA", "io5rMGhuv97FJPKrMtQZFlEnoJDrziz+nN4JsjlU", "vsp-userfiles-mobilehub-602139379")
# Calling the functions.
bawss3Object.uploadDataToS3("./fileToUpLoadFromLocal.jpg", "derek/nameToSaveAsToS3.jpg")
awss3Object.downloadDataFromS3("derek/test.jpg", "./nameToSaveAsToLocal.png")

