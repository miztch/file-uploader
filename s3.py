import boto3

s3 = boto3.client('s3')


def put_object(bucket_name, upload_data, object_key):
    result = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=upload_data
    )

    return result


def get_object(bucket_name, object_key):
    result = s3.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    return result


def generate_presigned_url(bucket_name, object_key):
    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=3600
    )

    return presigned_url
