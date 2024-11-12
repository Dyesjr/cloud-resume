import json
import boto3
from botocore.exceptions import ClientError
import os

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')
# table_name = 'VisitorCountTable'  
table_name = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    # Retrieve the current visitor count from DynamoDB
    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={'visitor_id': {'S': 'visitor_count'}}
        )
        
        # If the item doesn't exist, initialize the count to 0
        if 'Item' not in response:
            visitor_count = 0
        else:
            visitor_count = int(response['Item']['count']['N'])

        # Increment the visitor count
        visitor_count += 1

        # Update the count in DynamoDB
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'visitor_id': {'S': 'visitor_count'},
                'count': {'N': str(visitor_count)}
            }
        )

        # Return the updated count in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'visitor_count': visitor_count})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
