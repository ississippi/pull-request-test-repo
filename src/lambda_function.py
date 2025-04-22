import json

def lambda_handler(event, context):
    print("request:", json.dumps(event))
    body = json.loads(event['body']) if event.get('body') else {}
    pr_number = body.get('pr_number', 'unknown')
    pr_title = body.get('pr_title', 'unknown')
    repo = body.get('repo', 'unknown')
    html_url = body.get('html_url', 'unknown')
    user_login = body.get('user_login', 'unknown')
    created_at = body.get('created_at', 'unknown')
    pr_state = body.get('pr_state', 'unknown')
    base_ref = body.get('base_ref', 'unknown')
    pr_body = body.get('pr_body', 'unknown')

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': f'pr_number, {pr_number}!',
        'body': f'pr_title, {pr_title}!',
        'body': f'repo, {repo}!',
        'body': f'html_url, {html_url}!',
        'body': f'user_login, {user_login}!',
        'body': f'created_at, {created_at}!',
        'body': f'pr_state, {pr_state}!',
        'body': f'base_ref, {base_ref}!',
        'body': f'pr_body, {pr_body}!'
    }
    print("response:", json.dumps(response))
    return response
