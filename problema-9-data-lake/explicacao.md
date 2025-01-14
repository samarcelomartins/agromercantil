# Solução 
Estrutura dos Dados no Data Lake

#### Organização do Data Lake

1. **Camadas de Dados**:
   - **Camada de Ingestão**: Armazena dados brutos exatamente como foram recebidos.
   - **Camada de Processamento**: Contém dados processados, limpos e enriquecidos.
   - **Camada de Consumo**: Dados prontos para consumo pelo Data Warehouse e outras aplicações analíticas.

#### Estrutura de Diretórios

Organize os dados no Data Lake (Amazon S3) em um esquema de diretórios hierárquico para facilitar a navegação e o processamento:

```plaintext
s3://datalake/
    ingest/
        sales/
            year=2025/
                month=01/
                    day=14/
                        sales_data_20250114.csv
        customers/
            year=2025/
                month=01/
                    day=14/
                        customer_data_20250114.csv
    processing/
        sales/
            year=2025/
                month=01/
                    day=14/
                        sales_data_clean_20250114.csv
        customers/
            year=2025/
                month=01/
                    day=14/
                        customer_data_clean_20250114.csv
    consumption/
        sales/
            year=2025/
                month=01/
                    day=14/
                        sales_data_ready_20250114.parquet
        customers/
            year=2025/
                month=01/
                    day=14/
                        customer_data_ready_20250114.parquet
```

- **Ingestão**: Diretórios `ingest/sales/` e `ingest/customers/` organizados por ano, mês e dia.
- **Processamento**: Diretórios `processing/sales/` e `processing/customers/` para armazenar dados limpos.
- **Consumo**: Diretórios `consumption/sales/` e `consumption/customers/` para dados prontos para análise.

### 2. Política de Gerenciamento do Ciclo de Vida dos Dados no Data Lake

#### Política de Ciclo de Vida

1. **Armazenamento de Dados Brutos**:
   - Mantenha os dados na camada de ingestão por 90 dias para permitir reprocessamentos, se necessário.
   - Após 90 dias, mova os dados para a camada de arquivamento.

2. **Armazenamento de Dados Processados**:
   - Mantenha os dados na camada de processamento por 1 ano.
   - Após 1 ano, mova os dados para a camada de arquivamento.

3. **Armazenamento de Dados para Consumo**:
   - Mantenha os dados na camada de consumo por 3 anos.
   - Após 3 anos, mova os dados para a camada de arquivamento.

4. **Arquivamento e Exclusão**:
   - Dados arquivados podem ser armazenados no S3 Glacier para redução de custos.
   - Dados antigos (por exemplo, mais de 7 anos) podem ser excluídos permanentemente, conforme as políticas de retenção.

#### Exemplo de Configuração de Ciclo de Vida no S3

```json
{
   "Rules": [
      {
         "ID": "MoveIngestToArchive",
         "Prefix": "ingest/",
         "Status": "Enabled",
         "Transitions": [
            {
               "Days": 90,
               "StorageClass": "GLACIER"
            }
         ]
      },
      {
         "ID": "MoveProcessingToArchive",
         "Prefix": "processing/",
         "Status": "Enabled",
         "Transitions": [
            {
               "Days": 365,
               "StorageClass": "GLACIER"
            }
         ]
      },
      {
         "ID": "MoveConsumptionToArchive",
         "Prefix": "consumption/",
         "Status": "Enabled",
         "Transitions": [
            {
               "Days": 1095,
               "StorageClass": "GLACIER"
            }
         ]
      },
      {
         "ID": "DeleteOldData",
         "Prefix": "archive/",
         "Status": "Enabled",
         "Expiration": {
            "Days": 2555
         }
      }
   ]
}
```

### 3. Script de Integração de Dados do Data Lake ao Data Warehouse

#### Exemplo de Script em Python e SQL

O script a seguir lê dados do Data Lake (S3), processa-os e carrega-os no Data Warehouse (Redshift).

```python
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
```

### Explicação do Script

1. **Configurações**:
   - Define as configurações do bucket S3 e do cluster Redshift.

2. **Função `read_s3_data`**:
   - Utiliza o cliente `boto3` para listar e ler objetos no S3.
   - Carrega os dados de arquivos Parquet em um DataFrame `pandas`.

3. **Função `load_data_to_redshift`**:
   - Conecta ao cluster Redshift usando `psycopg2`.
   - Carrega os dados do DataFrame para o Redshift usando o comando `COPY`.

4. **Main Script**:
   - Lê os dados do Data Lake.
   - Carrega os dados no Data Warehouse.
   - Imprime uma mensagem de sucesso.

### Conclusão

Esta solução aborda a estruturação dos dados no Data Lake para facilitar o consumo no Data Warehouse, propõe uma política de gerenciamento do ciclo de vida dos dados e fornece um script de exemplo para integrar dados do Data Lake ao Data Warehouse utilizando Python e SQL. Essa abordagem garante uma gestão eficiente e segura dos dados, permitindo análises estruturadas e conformidade com políticas de retenção.

1. Escalabilidade: O Data Lake organiza dados brutos em um formato escalável e acessível.
2. Eficiência: Otimização no consumo de dados reduz custos de consulta no Redshift.
3. Automatização: Políticas de ciclo de vida e ETL automatizados simplificam a manutenção.
