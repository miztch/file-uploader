import datetime
import io

from flask import jsonify

import datastore
import util


def add(bucket, table, file, description):
    '''
    add file - into S3 bucket and dynamodb table
    '''
    file_id = util.generate_random_filename()
    extension = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    s3_key = '{}.{}'.format(file_id, extension)
    upload_data = io.BufferedReader(file).read()

    try:
        datastore.s3_put_object(
            bucket,
            upload_data,
            s3_key
        )

        datastore.dynamodb_put_item(
            table,
            {
                'file_id': file_id,
                'description': description,
                'timestamp': timestamp,
                's3_key': s3_key
            }
        )

        return jsonify({'Operation': 'add', 'Result': 'success'})
    except Exception as e:
        print(e)
        raise e


def get(bucket, table, file_id):
    '''
    get file by file_id from S3 bucket
    '''
    try:
        item = datastore.dynamodb_get_item(table, {'file_id': file_id})['Item']

        s3_key = item['s3_key']
        timestamp = item['timestamp']

        s3_object = datastore.s3_get_object(bucket, s3_key)

        presigned_url = datastore.s3_generate_presigned_url(bucket, s3_key)

        file = {
            'file_id': file_id,
            's3_key': s3_key,
            'timestamp': timestamp,
            'presigned_url': presigned_url
        }

        return file
    except Exception as e:
        print(e)
        raise e


def list(table):
    '''
    returns items in descending order by timestamp
    from dynamodb.scan() result
    '''
    response = datastore.dynamodb_scan(table)

    result = sorted(response['Items'],
                    key=lambda x: x['timestamp'], reverse=True)

    return result
