import boto3
import time

# Exemplo de envio de métrica personalizada para o CloudWatch
cloudwatch = boto3.client('cloudwatch')

def send_execution_time_metric(stage_name, execution_time):
    cloudwatch.put_metric_data(
        Namespace='MyPipelineMetrics',
        MetricData=[
            {
                'MetricName': 'ExecutionTime',
                'Dimensions': [
                    {
                        'Name': 'StageName',
                        'Value': stage_name
                    },
                ],
                'Value': execution_time,
                'Unit': 'Seconds'
            },
        ]
    )


# Exemplo de Configuração de Alarme no CloudWatch para Taxa de Erros
def send_error_rate_metric(stage_name, error_count):
    cloudwatch.put_metric_data(
        Namespace='MyPipelineMetrics',
        MetricData=[
            {
                'MetricName': 'ErrorRate',
                'Dimensions': [
                    {
                        'Name': 'StageName',
                        'Value': stage_name
                    },
                ],
                'Value': error_count,
                'Unit': 'Count'
            },
        ]
    )
