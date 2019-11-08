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


def store_image_object(image_id, image_binary):
    """ Store image on AWS S3. image_id should be the same as for DynamoDB.

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
    # TODO: return list of image_id for this user
    pass


def store_image_data(image_binary, username, description, privacy):
    """
    Store information on S3 and DynamoDB.
    DynamoDB table should consist at least on image_id, user_id, description, privacy (True or False), and tags.

    :param image_binary: binary file stored on S3 (I took care of this part)
    :param username: string, owner's name
    :param description: string, description of the image, can be an empty string
    :param privacy: boolean
    :return: None
    """
    image_id = utils.create_picID()
    # store image on AWS S3
    store_image_object(image_id, image_binary)
    # TODO: Write DynamoDB code storing all the image information
    # split tags
    # store image_id, description, tags, username, etc on DynamoDB
