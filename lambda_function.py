import json
import boto3
from datetime import datetime
import logging
from botocore.exceptions import ClientError

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def append_to_s3_object(bucket_name, key, new_data):
    s3 = boto3.client('s3')
    try:
        # Get the existing data from the object
        response = s3.get_object(Bucket=bucket_name, Key=key)
        existing_data = json.loads(response['Body'].read())

        # Append new data to existing data
        existing_data.append(new_data)
        
        # Write the updated data back to the object
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(existing_data))
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            # If the object doesn't exist, create a new one with the new data
            s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps([new_data]))
        else:
            # Handle other errors
            raise

def lambda_handler(event, context):
   
    print("Starting SQS Batch Process")
    logger.info('Received event: {}'.format(json.dumps(event)))

    print("Event Received : ", event)
    print("Data : ", event[0]['body'])

    message = event[0]['body']
    
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Define the bucket name where you want to store the data
    bucket_name = 'airbnb-booking-records-sm'
    
    # Set key as "BookingDetails_" + timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    key = f"BookingDetails_{timestamp}.json"
        
    append_to_s3_object(bucket_name, key, message)
    
    print("Ending SQS Batch Process")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data written to S3 successfully')
    }
