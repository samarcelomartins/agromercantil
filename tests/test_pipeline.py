import unittest
from unittest.mock import patch, Mock
import pandas as pd
from pipeline import read_s3_data, calculate_average

class TestPipeline(unittest.TestCase):

    @patch('pipeline.boto3.client')
    def test_read_s3_data(self, mock_boto_client):
        # Configura o mock para simular a resposta do S3
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3
        mock_s3.get_object.return_value = {
            'Body': Mock(read=Mock(return_value=b'id,log_time,log_data\n1,2025-01-01T00:00:00Z,100\n2,2025-01-02T00:00:00Z,200'))
        }

        # Chama a função para ler os dados do S3
        df = read_s3_data('fake-bucket', 'fake-key')

        # Verifica se o DataFrame foi criado corretamente
        expected_df = pd.DataFrame({
            'id': [1, 2],
            'log_time': ['2025-01-01T00:00:00Z', '2025-01-02T00:00:00Z'],
            'log_data': [100, 200]
        })
        pd.testing.assert_frame_equal(df, expected_df)

    def test_calculate_average(self):
        # Cria um DataFrame de exemplo
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [100, 200, 300]
        })

        # Chama a função para calcular a média
        average_value = calculate_average(df, 'value')

        # Verifica se a média está correta
        self.assertEqual(average_value, 200)

if __name__ == '__main__':
    unittest.main()
