# Flask Version
import json
import boto3
from flask import Flask, request

app = Flask(__name__)

def flask_lambda_handler(event, context):
    # Handle both string and dict body inputs
    body = event.get('body', {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON in body'}),
                'headers': {'Content-Type': 'application/json'}
            }
    elif not isinstance(body, dict):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Body must be a JSON string or dictionary'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    # Simulate Flask request context
    with app.test_request_context(
        path=event.get('path', '/'),
        method=event.get('httpMethod', 'POST'),
        json=body,
        headers=event.get('headers', {})
    ):
        try:
            # Extract relevant fields
            pr_number = body.get('pr_number')
            repo = body.get('repo')
            pr_title = body.get('pr_title')
            user_login = body.get('user_login')
            html_url = body.get('html_url')
            
            # Construct SNS message
            sns_message = {
                'pr_number': pr_number,
                'repository': repo,
                'title': pr_title,
                'user': user_login,
                'url': html_url
            }
            
            # Initialize SNS client and publish message to FIFO topic
            sns_client = boto3.client('sns')
            response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:238338230919:pr-review-standard',
                Message=json.dumps(sns_message),
                Subject=f'New Pull Request #{pr_number}'
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'SNS message sent successfully',
                    'sns_response': response
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e)
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }