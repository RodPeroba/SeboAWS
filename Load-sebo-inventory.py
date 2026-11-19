import json
import urllib
import boto3
import csv

# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
inventoryTable = dynamodb.Table('inventario-sebo')

# This handler is run every time the Lambda function is invoked


def lambda_handler(event, context):

    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))

    # Get the bucket and object key from the Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    localFilename = '/tmp/inventarioSebo.txt'

    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, localFilename)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    with open(localFilename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        rowCount = 0
        for row in reader:
            rowCount += 1
            print(row['livro'], row['quantidade'])

            try:
                # Insere livro e quantidade no inventário
                inventoryTable.put_item(
                    Item={
                        'NomeDoLivro': row['livro'],
                        'Quantidade': int(row['quantidade'])})
                # Pode haver um problema com dois itens iguais !!!
            except Exception as e:
                print(e)
                print("Unable to insert data into DynamoDB table".format(e))

    return "%d counts inserted" % rowCount
