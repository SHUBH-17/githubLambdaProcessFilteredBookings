import json
import boto3
from datetime import datetime
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
   
    print("Starting SQS Batch Process")
  
    logger.info('Received event: {}'.format(json.dumps(event)))
    print("Event Received : ", event)
    print("Data : ", event[0]['body'])

    sqs_msg = json.loads(event[0]['body'])
    print ('SQS Message: ', sqs_msg)

    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Define the bucket name where you want to store the data
    bucket_name = 'airbnb-booking-records-sm'
    
    # Set key as "BookingDetails_" + timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    key = f"BookingDetails_{timestamp}.json"

    Response = s3.put_object(Bucket=bucket_name, Key=key, Body = sqs_msg)
        
    print("Ending SQS Batch Process")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data written to S3 successfully')
    }
