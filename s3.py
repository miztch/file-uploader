import boto3


def init_resource(bucket_name):
    s3 = boto3.resource('s3')
    Bucket = s3.Bucket(bucket_name)
    return Bucket


def list_object(bucket_name):
    Bucket = init_resource(bucket_name)

    result = Bucket.objects.all()
    return result


def put_object(bucket_name, upload_data, object_key):
    Bucket = init_resource(bucket_name)

    result = Bucket.put_object(Key=object_key, Body=upload_data)
    return result


def generate_presigned_url(bucket_name, object_key):
    s3 = boto3.client('s3')

    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_key},
        ExpiresIn=3600,
        HTTPMethod='GET'
    )

    return presigned_url
