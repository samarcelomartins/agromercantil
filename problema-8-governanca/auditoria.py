import boto3

cloudtrail = boto3.client('cloudtrail')

def check_access_logs():
    response = cloudtrail.lookup_events(
        LookupAttributes=[
            {'AttributeKey': 'EventName', 'AttributeValue': 'GetObject'}
        ],
        MaxResults=10
    )
    for event in response['Events']:
        print(f"Evento: {event['EventName']} - Usuário: {event['Username']}")

check_access_logs()
