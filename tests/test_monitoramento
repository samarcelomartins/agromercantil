from unittest.mock import Mock

def test_monitoramento_cloudwatch(mocker):
    mock_cloudwatch = Mock()
    mocker.patch('boto3.client', return_value=mock_cloudwatch)
    mock_cloudwatch.get_metric_statistics.return_value = {
        'Datapoints': [{'Sum': 2}]
    }
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/Glue',
        MetricName='FailedJobs',
        StartTime='2023-01-01T00:00:00Z',
        EndTime='2023-01-01T01:00:00Z',
        Period=60,
        Statistics=['Sum']
    )
    assert response['Datapoints'][0]['Sum'] == 2
