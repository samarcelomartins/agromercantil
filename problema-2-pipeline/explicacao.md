# Solução Proposta

## Explicação do Script

1. Configurações do S3: Definimos o nome do bucket e a chave do objeto (caminho para o arquivo).
2. Função read_s3_data: Utiliza o boto3 para ler os dados do S3 e carrega em um DataFrame do pandas.
3. Função calculate_average: Calcula a média de uma coluna específica no DataFrame.
4. Função main: Orquestra a leitura dos dados do S3 e a aplicação da transformação, exibindo os resultados no console.
