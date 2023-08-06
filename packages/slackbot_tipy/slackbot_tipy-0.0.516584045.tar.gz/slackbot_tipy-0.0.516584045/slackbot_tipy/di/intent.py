import boto3
from boto3.dynamodb.conditions import Key

# connect to Dynamo
try:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('answersnow_prompts')
except:
    print('unable to connect to db')

def decipher_intent(prompt_name, user_response):
    print(prompt_name,user_response)

    #node = monty_response[prompt_name]
    node = table.query(
        KeyConditionExpression=Key('prompt_now').eq(prompt_name)
        )['Items'][0]['prompt']
    
    # Essentially, return next prompt
    if not user_response:
        return prompt_name, node['text'], True if len(node['responses']) == 0 else False
    else:
        for resp in node['responses'].keys():
            response = node['responses'][resp]
            for word in response['utterances'].split(","):
                if word.strip() in user_response.lower():
                    return decipher_intent(response['next_prompt'],None)
        return (prompt_name,'-> ' + node['text'],False)
    
