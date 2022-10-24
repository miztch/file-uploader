import boto3

def init(table_name):
    dynamodb = boto3.resource('dynamodb')
    Table = dynamodb.Table(table_name)
    return Table


def scan(table_name):
    Table = init(table_name)

    return Table.scan()

def get_all(table_name):
    Table = init(table_name)

    response = Table.scan()
    result = response['Items']

    return result


def put(table_name, item):
    Table = init(table_name)
    result = Table.put_item(Item=item)

    return result
