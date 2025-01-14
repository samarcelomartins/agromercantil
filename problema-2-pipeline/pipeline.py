import boto3
import pandas as pd
import io

# Configurações do S3
s3_bucket = 'nome-do-seu-bucket'
s3_key = 'caminho/para/seu/arquivo.csv'

# Função para ler dados do S3
def read_s3_data(bucket, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read()
    df = pd.read_csv(io.BytesIO(data))
    return df

# Função para calcular a média de um campo
def calculate_average(df, column_name):
    return df[column_name].mean()

def main():
    # Ler os dados do S3
    df = read_s3_data(s3_bucket, s3_key)
    print("Dados lidos do S3:")
    print(df.head())

    # Calcular a média de um campo específico
    average_value = calculate_average(df, 'nome_da_coluna')
    print(f"A média do campo 'nome_da_coluna' é: {average_value}")

if __name__ == "__main__":
    main()
