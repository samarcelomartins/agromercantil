# Solução Proposta

## Arquitetura do Pipeline:
1. Ingestão:
* Dados IoT são armazenados no Amazon S3 em uma estrutura organizada (ex.: /raw/YYYY/MM/DD).

2. Processamento:
* Usar AWS Glue para executar transformações em lote.
* Alternativa: usar Apache Spark no Amazon EMR para maior flexibilidade.

3. Armazenamento:
* Salvar os dados processados no S3 em uma camada "curated".
* Carregar os resultados no Amazon Redshift para análises estruturadas.

## Explicação do Script

1. Configurações do S3: Definimos o nome do bucket e a chave do objeto (caminho para o arquivo).
2. Função read_s3_data: Utiliza o boto3 para ler os dados do S3 e carrega em um DataFrame do pandas.
3. Função calculate_average: Calcula a média de uma coluna específica no DataFrame.
4. Função main: Orquestra a leitura dos dados do S3 e a aplicação da transformação, exibindo os resultados no console.

# Benefícios:
1. Escalabilidade: Soluções AWS como Glue e Redshift são otimizadas para grandes volumes.
2. Organização: Separar dados "raw" e "curated" facilita a governança.
3. Automação: O uso de pipelines automatizados reduz erros manuais.
