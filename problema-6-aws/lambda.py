import json
import boto3

def lambda_handler(event, context):
    # Conexão com o S3
    s3 = boto3.client('s3')
    bucket_name = 'meu-bucket'
    
    # Processa eventos recebidos do Kinesis
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        # Exemplo: transformação simples
        processed_data = {"id": payload["id"], "valor": payload["valor"] * 2}
        
        # Salva dados processados no S3
        key = f"processed/{payload['id']}.json"
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(processed_data))
    
    return {"statusCode": 200, "body": "Dados processados e armazenados no S3"}
