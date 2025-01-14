import boto3
import pandas as pd
import psycopg2
from io import StringIO

# Configurações AWS e Redshift
s3_bucket = 'datalake'
s3_prefix = 'consumption/sales/year=2025/month=01/day=14/'
redshift_host = 'redshift-cluster-1.xxxxxx.us-west-2.redshift.amazonaws.com'
redshift_db = 'mydb'
redshift_user = 'myuser'
redshift_password = 'mypassword'
redshift_port = 5439
redshift_table = 'sales'

# Função para ler dados do S3
def read_s3_data(bucket, prefix):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    data_frames = []
    
    for obj in response.get('Contents', []):
        s3_object = s3_client.get_object(Bucket=bucket, Key=obj['Key'])
        df = pd.read_parquet(s3_object['Body'])
        data_frames.append(df)
    
    return pd.concat(data_frames, ignore_index=True)

# Função para carregar dados no Redshift
def load_data_to_redshift(df, table):
    conn = psycopg2.connect(
        dbname=redshift_db,
        user=redshift_user,
        password=redshift_password,
        host=redshift_host,
        port=redshift_port
    )
    cursor = conn.cursor()
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    cursor.copy_expert(f"COPY {table} FROM STDIN WITH CSV NULL AS ''", buffer)
    conn.commit()
    cursor.close()
    conn.close()

# Main script
if __name__ == "__main__":
    # Ler dados do Data Lake
    sales_data = read_s3_data(s3_bucket, s3_prefix)
    
    # Carregar dados no Redshift
    load_data_to_redshift(sales_data, redshift_table)
    
    print("Dados carregados com sucesso no Redshift.")
