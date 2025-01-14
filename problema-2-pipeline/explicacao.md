Configurações do S3: Definimos o nome do bucket e a chave do objeto (caminho para o arquivo).
Função read_s3_data: Utiliza o boto3 para ler os dados do S3 e carrega em um DataFrame do pandas.
Função calculate_average: Calcula a média de uma coluna específica no DataFrame.
Função main: Orquestra a leitura dos dados do S3 e a aplicação da transformação, exibindo os resultados no console.
