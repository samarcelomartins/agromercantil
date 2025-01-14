# Solução Proposta

## Estratégia para Configurar um Scraper Resiliente:

1. Evitar bloqueios:
* Rotação de proxies: Use serviços como ProxyMesh ou Bright Data para mudar o endereço IP a cada requisição. Isso ajuda a evitar bloqueios baseados em IP..
* Alteração de User-Agent: Simule navegadores reais (ex.: Chrome, Firefox) incluindo o agente do usuário, cookies e cabeçalhos de referenciador. Isso ajuda a evitar a detecção de bots..

2. Atrasos randômicos: Insira intervalos variáveis entre as requisições para imitar comportamento humano. Isso ajuda a evitar a detecção de padrões de scraping.

3. Detectar mudanças no layout:
* Usar ferramentas como BeautifulSoup ou selenium para capturar o HTML. Implemente verificações para detectar mudanças no layout HTML e ajustar o scraper automaticamente.
* Monitorar alterações nos elementos-chave (ex.: tags, IDs, classes).

4. Autenticação e Captcha:
* Implementar automação com selenium para lidar com logins e captchas. Use um gerenciador de sessões para manter cookies e simular uma navegação contínua, como se fosse um navegador real.
* Usar APIs como 2Captcha para resolver captchas automaticamente.

## Explicação do Código
1. Função get_page_content:
* Faz uma requisição GET para a URL especificada usando os cabeçalhos fornecidos e retorna o conteúdo da página.

2. Função calculate_hash:
* Calcula o hash MD5 do conteúdo HTML da página para detectar mudanças no layout.

3. Função detect_layout_changes:
* Compara o hash do conteúdo atual com o hash anterior para detectar mudanças no layout.
* Imprime uma mensagem se uma mudança no layout for detectada.

4. Cabeçalhos:
Define cabeçalhos que imitam um navegador real para evitar a detecção de bots.

5. Loop de Scraping:
* Executa o scraping e a detecção de mudanças no layout 5 vezes como exemplo.
* Introduz atrasos aleatórios entre as requisições para imitar comportamento humano.

## Explicação dos Testes Unitários
1. Testando get_page_content:
* Usa patch para substituir requests.get com um mock que retorna um conteúdo de página fictício.
* Verifica se get_page_content retorna o conteúdo esperado.

2. Testando calculate_hash:
* Verifica se calculate_hash retorna o hash MD5 correto para um conteúdo de página fictício.

3. Testando detect_layout_changes:
* Usa patch para substituir get_page_content com um mock que retorna dois conteúdos diferentes.
* Verifica se detect_layout_changes detecta corretamente uma mudança no layout entre duas chamadas consecutivas.

# Benefícios:
Este exemplo demonstra como configurar um scraper resiliente usando Python e BeautifulSoup. 
Ele inclui práticas recomendadas para evitar bloqueios, como rotação de IPs, atrasos aleatórios e uso de cabeçalhos realistas. 
O código também detecta mudanças no layout da página comparando hashes do conteúdo HTML.

1. Resiliência: O scraper é capaz de lidar com mudanças no layout e bloqueios.
2. Automatização: Scripts podem ser agendados para execução periódica.
3. Escalabilidade: Soluções como proxies permitem monitorar vários produtos simultaneamente.
