"""
Call AWS services from here!
"""
import boto3
import utils
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


def store_image_object(image_binary):
    """ Store image on AWS S3.

    :param image_binary: binary file from user
    :return None
    """
    pass


def get_all_images(username):
    """
    Retrieve all image names from DynamoDB

    :param username: owner's name associated with images
    :return: array of strings, names of all images for this user
    """


def store_image_data():
    image_id = utils.create_picID()
    pass
