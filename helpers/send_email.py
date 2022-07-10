from config.keys import AWS_REGION
from django.http import JsonResponse
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


region = Config(
        region_name=AWS_REGION,
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
            }
    )
client = boto3.client('ses', config=region)

def send_email(recipient, sender, subject, message):
    response = client.send_email(
        Destination={
            'ToAddresses': [
                recipient
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': message
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'This is the message body in text format.',
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender,
        ReplyToAddresses=[
            sender,
        ],
    )
    print(response)
    return response