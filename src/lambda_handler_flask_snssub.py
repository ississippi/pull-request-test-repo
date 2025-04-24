# Flask Version
import json
import boto3
from flask import Flask, request

app = Flask(__name__)

def flask_lambda_handler(event, context):
    try:
        # SNS sends a list of records; process the first one
        sns_record = event['Records'][0]['Sns']
        message = sns_record['Message']
        
        # Parse the SNS message
        message_data = json.loads(message)
        
        # Simulate Flask request context with message data
        with app.test_request_context(json=message_data):
            # Extract fields
            pr_number = message_data.get('pr_number')
            repository = message_data.get('repository')
            title = message_data.get('title')
            user = message_data.get('user')
            url = message_data.get('url')
            
            # Log the extracted data (replace with your processing logic)
            log_message = (
                f"Received SNS message:\n"
                f"PR Number: {pr_number}\n"
                f"Repository: {repository}\n"
                f"Title: {title}\n"
                f"User: {user}\n"
                f"URL: {url}"
            )
            
            # Use CloudWatch Logs via print
            print(log_message)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'SNS message processed successfully',
                    'data': message_data
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            
    except Exception as e:
        print(f"Error processing SNS message: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }