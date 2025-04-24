# Raw Lambda Handler Version
import json
import boto3

def lambda_handler(event, context):
    # Extract body from event
    try:
        body = event.get('body', {})
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            raise ValueError("Body is not a valid JSON string or dictionary")
            
        # Extract relevant fields
        pr_number = body.get('pr_number')
        repo = body.get('repo')
        pr_title = body.get('pr_title')
        user_login = body.get('user_login')
        html_url = body.get('html_url')
        created_at = body.get('created_at')
        pr_state = body.get('pr_state')
        base_ref = body.get('base_ref')
        
        # Construct SNS message
        sns_message = {
            'pr_number': pr_number,
            'repo': repo,
            'pr_title': pr_title,
            'user_login': user_login,
            'url': html_url,
            'created_at': created_at,
            'pr_state': pr_state,
            'base_ref': base_ref
        }
        
        # Initialize SNS client and publish message
        sns_client = boto3.client('sns')
        response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:238338230919:pr-review-standard',  # Replace with your SNS Topic ARN
            Message=json.dumps(sns_message),
            Subject=f'New Pull Request #{pr_number}'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'SNS message sent successfully',
                'sns_response': response
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

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
            created_at = body.get('created_at')
            pr_state = body.get('pr_state')
            base_ref = body.get('base_ref')
            
            # Construct SNS message
            sns_message = {
                'pr_number': pr_number,
                'repo': repo,
                'pr_title': pr_title,
                'user_login': user_login,
                'url': html_url,
                'created_at': created_at,
                'pr_state': pr_state,
                'base_ref': base_ref
            }
            
            # Initialize SNS client and publish message
            sns_client = boto3.client('sns')
            response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:238338230919:pr-request.fifo',  # Replace with your SNS Topic ARN
                Message=json.dumps(sns_message),
                Subject=f'New Pull Request #{pr_number}',
                MessageGroupId=str(pr_number)  # Use pr_number as MessageGroupId for FIFO
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