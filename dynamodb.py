import boto3

dynamodb = boto3.resource('dynamodb')


def get_all(table_name):
    Table = dynamodb.Table(table_name)

    response = Table.scan()
    result = sorted(response['Items'],
                    key=lambda x: x['timestamp'], reverse=True)

    return result


def get(table_name, file_id):
    Table = dynamodb.Table(table_name)

    result = Table.get_item(Key={'file_id': file_id})

    return result


def put(table_name, item):
    Table = dynamodb.Table(table_name)

    result = Table.put_item(Item=item)

    return result
