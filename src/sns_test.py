import boto3
import json
import env

def sent_sns_test_messsage():
    snsClient = boto3.client(
        'sns', 
        aws_access_key_id=env.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
        region_name=env.AWS_REGION)
    topic_arn = env.SNS_TOPIC_ARN

    message = {
        "pr_number": 123,
        "pr_title": "Test PR",
        "repo": "test-repo",
        "user_login": "test-user",
        "created_at": "2023-10-01T12:00:00Z"
    }
    
    response = snsClient.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        Subject='Test SNS Message'
    )
    
    print(f"Message sent to SNS topic {topic_arn}: {response}")