# Raw Lambda Handler Version
import json
import boto3

def lambda_handler(event, context):
    try:
        # SNS sends a list of records; process the first one
        sns_record = event['Records'][0]['Sns']
        message = sns_record['Message']

        # Parse the SNS message
        message_data = json.loads(message)
        print(f"Received SNS message data: {message_data}")

        # Extract fields
        pr_number = message_data.get('pr_number')
        repository = message_data.get('repo')
        title = message_data.get('pr_title')
        user = message_data.get('user_login')
        url = message_data.get('url')
        created_at = message_data.get('created_at')
        pr_state = message_data.get('pr_state')
        base_ref = message_data.get('base_ref')
        
        # Log the extracted data (replace with your processing logic)
        # log_message = (
        #     f"Received SNS message:\n"
        #     f"PR Number: {pr_number}\n"
        #     f"Repository: {repository}\n"
        #     f"Title: {title}\n"
        #     f"User: {user}\n"
        #     f"URL: {url}\n"
        #     f"created_at: {created_at}\n"
        #     f"pr_state: {pr_state}\n"
        #     f"base_ref: {base_ref}\n"
        # )
        
        # Use CloudWatch Logs via print (boto3 logger can be used if needed)
        # print(log_message)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'SNS message processed successfully',
                'data': message_data
            })
        }
        
    except Exception as e:
        print(f"Error processing SNS message: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
