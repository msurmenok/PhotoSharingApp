"""
Call AWS services from here!
"""
import boto3
from botocore.exceptions import ClientError


def get_s3_image(image_id):
    """ Retrieve an object from AWS S3.

    :param image_id: string
    :return binary representation of an object. If it does not exist, return None
    """
    s3 = boto3.client('s3')
    try:
        return s3.get_object(Bucket='photosharingapp-test', Key=image_id)['Body'].read()
    except ClientError as e:
        print(e)
        return None