"""
SJSU CS 218 Fall 2019 TEAM 4

Call AWS S3 and DynamoDB services from here.
"""
import boto3
import utils
from image import Image
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

TABLE_NAME = "Image"

BUCKET_NAME = 'photo-sharing-app-project'
REGION_NAME = 'us-west-2'


def get_s3_image(image_id):
    """ Retrieve an object from AWS S3.

    :param image_id: string
    :return binary representation of an object. If it does not exist, return None
    """
    s3 = boto3.client('s3', region_name=REGION_NAME)
    try:
        return s3.get_object(Bucket=BUCKET_NAME, Key=image_id)['Body'].read()
    except ClientError as e:
        print(e)
        return None


def get_dynamodb_image(image_id):
    """
    Retrieve an image data with the specific key from dynamo_db

    :param image_id: string, image key in dynamodb
    :return: object Image
    """
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(
        Key={
            'image_id': image_id
        }
    )
    item = response['Item']
    image_id = item["image_id"]
    username = item["username"]
    description = item["description"]
    tags = item["tags"]
    privacy = item["privacy"]
    return Image(image_id=image_id, username=username, description=description, tags=tags, privacy=privacy)


def store_image_object(image_id, image_binary):
    """ Store image on AWS S3. image_id should be the same as for DynamoDB.

    :param image_id: string that uniquely identifies this image
    :param image_binary: binary file from user, jpg or jpeg
    :return None
    """
    image_name = image_id + ".jpg"
    s3_client = boto3.client('s3', region_name=REGION_NAME)
    try:
        response = s3_client.upload_fileobj(image_binary, BUCKET_NAME, image_name)
    except ClientError as e:
        print(e)


def delete_image_object(image_id):
    """
    Delete image from AWS S3.

    :param image_id: string that uniquely identifies this image
    :return: True if deleted successfully
    """
    image_name = image_id + ".jpg"
    print(image_name)
    s3 = boto3.resource("s3", region_name=REGION_NAME)
    try:
        obj = s3.Object(BUCKET_NAME, image_name)
        response = obj.delete()
    except ClientError as e:
        print(e)
        return False
    print("Deleted from S3!")
    print(response)
    return True


def get_all_user_images(username):
    """
    Retrieve all image names from DynamoDB

    :param username: owner's name associated with images
    :return: array of Image objects that contains all the information about each image
    """
    # Retrieving all files from S3 and faking other data for Image object
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(
        FilterExpression=Attr('username').eq(username)
    )

    images_data = list()
    for obj in response.get("Items"):
        image_id = obj["image_id"]
        description = obj["description"]
        tags = obj["tags"]
        privacy = obj["privacy"]
        images_data.append(
            Image(image_id=image_id, username=username, description=description, tags=tags, privacy=privacy))
    return images_data


def get_all_public_images():
    """
    Retrieve all public images from DynamoDB

    :return: array of IMage objects that contains all the information about each public image
    """
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(
        FilterExpression=Attr('privacy').eq(False)
    )

    images_data = list()
    for obj in response.get("Items"):
        image_id = obj["image_id"]
        description = obj["description"]
        tags = obj["tags"]
        privacy = obj["privacy"]
        username = obj["username"]
        images_data.append(
            Image(image_id=image_id, username=username, description=description, tags=tags, privacy=privacy))
    return images_data


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
    image_id = utils.create_picID(username)
    # store image on AWS S3
    store_image_object(image_id, image_binary)
    # get tags from the description
    tags = utils.split_by_tag(description)
    # store image_id, description, tags, username, etc on DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    try:
        response = table.put_item(
            Item={
                'image_id': image_id,
                'username': username,
                'description': description,
                'tags': tags,
                'privacy': privacy
            }
        )
    except ClientError as e:
        print(e)
    print("End of store_image_data")


def delete_image_data(image_id):
    """
    Delete information about specific image from DynamoDB and S3.

    :param image_id: string that uniquely identifies image data in DynamoDB and S3
    :return: None
    """
    # If was successfully deleted from S3 then delete from DynamoDB
    if delete_image_object(image_id):
        dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
        table = dynamodb.Table(TABLE_NAME)
        try:
            table.delete_item(
                Key={
                    'image_id': image_id
                }
            )
        except ClientError as e:
            print(e)


def update_image_data(image_id, description, privacy):
    """
    Update description and privacy setting for the specified image in DynamoDB

    :param image_id: string uniequely idnetifies image data in DynamoDB
    :param description: string description to update
    :param privacy: boolean True if the image should be private
    :return: None
    """
    dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
    table = dynamodb.Table(TABLE_NAME)
    try:
        table.update_item(
            Key={
                'image_id': image_id
            },
            UpdateExpression='SET description = :val1, privacy = :val2',
            ExpressionAttributeValues={
                ':val1': description,
                ':val2': privacy
            }
        )
    except ClientError as e:
        print(e)
