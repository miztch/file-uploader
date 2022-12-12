import os

import boto3

s3 = boto3.client('s3', region_name=os.environ['AWS_REGION'])
dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])


def s3_put_object(bucket_name, upload_data, object_key):
    result = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=upload_data
    )

    return result


def s3_get_object(bucket_name, object_key):
    result = s3.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    return result


def s3_generate_presigned_url(bucket_name, object_key):
    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=3600
    )

    return presigned_url


def dynamodb_scan(table_name):
    Table = dynamodb.Table(table_name)

    result = Table.scan()

    return result


def dynamodb_get_item(table_name, key):
    Table = dynamodb.Table(table_name)

    result = Table.get_item(Key=key)

    return result


def dynamodb_put_item(table_name, item):
    Table = dynamodb.Table(table_name)

    result = Table.put_item(Item=item)

    return result
