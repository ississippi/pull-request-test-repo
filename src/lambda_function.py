import json

def lambda_handler(event, context):
    print("request:", json.dumps(event))
    body = json.loads(event['body']) if event.get('body') else {}
    pr_number = event['pr_number']
    pr_title = event['pr_title']
    repo = event['repo']
    html_url = event['html_url']
    user_login = event['user_login']
    created_at = event['created_at']
    pr_state = event['pr_state']
    base_ref = event['base_ref']
    pr_body = event['pr_body']

    response_body = {
        "pr_title": pr_title,
        "input": event
    }
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        "body": json.dumps(response_body)
    }
    print(f"Pull Request: {pr_number}: {pr_title} in {repo} by {user_login} at {created_at}")
    print("response:", json.dumps(response))
    return response