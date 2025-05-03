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
        
        # Construct SNS message
        sns_message = {
            'pr_number': pr_number,
            'repository': repo,
            'title': pr_title,
            'user': user_login,
            'url': html_url
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
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
