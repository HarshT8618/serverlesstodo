import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ToDoTable')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == "POST":
        data = json.loads(event['body'])
        task_id = str(uuid.uuid4())
        task_name = data.get("taskName", "Untitled Task")
        
        table.put_item(Item={'taskId': task_id, 'taskName': task_name})
        return {"statusCode": 200, "body": json.dumps({"message": "Task added", "taskId": task_id})}
    
    elif http_method == "GET":
        tasks = table.scan().get('Items', [])
        return {"statusCode": 200, "body": json.dumps(tasks)}
    
    elif http_method == "DELETE":
        data = json.loads(event['body'])
        task_id = data.get("taskId")
        
        table.delete_item(Key={'taskId': task_id})
        return {"statusCode": 200, "body": json.dumps({"message": "Task deleted"})}
    
    return {"statusCode": 400, "body": json.dumps({"message": "Invalid request"})}
