# O módulo requests abaixo é utilizado para fazermos as requisições HTTP
# Leia mais sobre este módulo em: https://docs.python-requests.org/
import requests
from datetime import datetime

# Método que faz as requisições utilizando a API REST (v3).
def rest_request(url, parameters = {}, headers = {}):
    # Neste exemplo, eu estou criando uma sessão para fazer as requisições.
    # Existem maneiras mais simples de se fazer uma requisição, como mostra
    # o método graphql_request em exemplo_graphql.py
    session = requests.Session()
    # Coloque abaixo seu usuário e o seu token de autenticação
    # Recomendo vocês criarem um token pessoal de acesso, como mostra o tutorial:
    # https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
    session.auth = ('SEU_USUARIO_AQUI', 'SEU_TOKEN_AQUI')

    # Realizamos a requisição à API via URL passando parâmetros e cabeçalhos quando necessário.
    response = session.get(url, params=parameters, headers=headers)

    # Nós temos um limite de requisições que podemos fazer em um determinado
    # período de tempo. Por isso, utilizem os valores abaixo provenientes 
    # das respostas dadas pela API para realizar novas requisições quando possível.

    response_headers = response.headers
    # O valor abaixo representa o número de requisições ainda disponível
    requests_remaining = response_headers['X-RateLimit-Remaining']
    print('Requests Remaining: ' + requests_remaining)
    # O valor abaixo representa a data/horário de quando o número de requisições vai reiniciar
    response_reset_datetime = response_headers['X-RateLimit-Reset']
    reset_time = datetime.fromtimestamp(int(response_reset_datetime)).strftime('%Y-%m-%d %H:%M:%S')
    print('Limit will reset at: ' + reset_time)
    # Sugestão: Quando o limite de requisições for igual a zero, coloque o seu processo em
    # estado de espera, até que a data de reinício seja atingida.

    # Retornamos a resposta dada pela API
    return response

def example_one():
    # Exemplo 1:
    # Coletando informações básicas de um repositório via REST
    # O repositório que vamos coletar é o vscode da microsoft

    # Definimos o caminho até o repositório na API montando uma URL
    url = 'https://api.github.com/repos/microsoft/vscode'
    # Requisitamos as informações dadas por tal caminho a API
    response = rest_request(url)
    # Transformamos a resposta dada pela API em JSON (Interpretado como dicionário em Python)
    json_values = response.json()
    # Manipulamos o dicionário de acordo com o que desejamos coletar.
    # No exemplo abaixo eu estou coletando o nome da licença do repositório.
    print(json_values['license']['name'])

def example_two():
    # Exemplo 2:
    # Coletando informações básicas de um usuário via REST
    # O usuário do qual vamos coletar informação é o fronchetti

    # Definimos o caminho até o usuário na API montando uma URL
    # Repare que a estrutura de uma URL para alcançar um usuário é diferente 
    # da estrutura para alcançar um repositório.
    url = 'https://api.github.com/users/fronchetti'
    # Requisitamos as informações dadas por tal caminho a API
    response = rest_request(url)
    # Transformamos a resposta dada pela API em JSON (Interpretado como dicionário em Python)
    json_values = response.json()
    # Manipulamos o dicionário de acordo com o que desejamos coletar.
    # No exemplo abaixo eu estou coletando a biografia do usuário. 
    print(json_values['bio'])

def example_three():
    # exemplo 3:
    # Coletando pull-requests _abertos_ de um repositório via REST 
    # Vamos utilizar o repositório vscode da microsoft novamente.

    # Definimos o caminho até os pull-requets do repositório montando uma URL
    url = 'https://api.github.com/repos/microsoft/vscode/pulls'
    # Definimos os parâmetros da nossa requisição. Neste caso, queremos apenas 
    # pull-requests abertos, então vou utilizar o parâmetro state.
    # Para saber quais parâmetros você pode utilizar para cada tipo de requisição, 
    # consulte a documentação. 
    # Neste exemplo, a página da documentação é esta:
    # https://docs.github.com/en/rest/reference/pulls#list-pull-requests
    parameters = {'state': 'open'}
    # requisitamos as infomações dadas por tal caminho a API
    response = rest_request(url=url, parameters=parameters)
    # Transformamos a resposta dada pela API em JSON (Interpretado como dicionário em Python)
    json_values = response.json()

    # Neste caso, a resosta é uma lista de dicionários, por isso
    # usamos um loop para percorrer todos os pull-requests.

    # No loop abaixo estamos percorrendo os pull-requests e imprimindo o título deles.
    for pull_request in json_values:
        print(pull_request['title'])

def example_four():
    # Exemplo 4:
    # Iterando páginas na API REST
    # Quando você tentar requisitar um tipo de informação que contém muitos dados,
    # por exemplo, todos os commits de um projeto, perceberá que ao requisitar uma única 
    # vez, nem todos os commits do projeto serão retornados. 
    # A API impõe um limite de informações retornadas a cada requisição,
    # por isso é preciso utilizar o sistema de páginação fornecido por ela para coletar
    # todos os dados que desejamos.

    # No exemplo abaixo iremos coletar todos os pull-requests abertos do exemplo três. 
    # Perceba que no exemplo três nem todos os pull-requests abertos do vscode são retornados, por isso 
    # precisamos iterar entre as páginas. 
    url = 'https://api.github.com/repos/microsoft/vscode/pulls'
    parameters = {'state': 'open'}
    next_page_available = True

    # Pra iterar entre páginas, o GitHub retorna a cada requisição um conjunto de links com informações tais como
    # quantas páginas existem para aquele tipo de informação, qual é a última página, etc.
    # No código abaixo, enquanto houver um 'next' no conjunto de links, eu prossigo pra próxima página, 
    # atualizando a URL atual. O resto do código é similar aos exemplos passados.
    while(next_page_available):
        print(url)
        response = rest_request(url=url, parameters=parameters)
        pagination_urls = response.links # Imprima esta variável caso queira ver as URLs fornecidas pela GitHub API

        if 'next' in pagination_urls:
            url = pagination_urls['next']['url']
        else:
            next_page_available = False # Quando não houver próxima página, terminamos o laço de repetição

def example_five():
    # Exemplo 5:
    # Coletando todos os pull requests abertos do projeto vscode.
    # Neste exemplo temos uma combinação de todos os quatro exemplos acima. 
    # Montando a URL, utilizamos parâmetros, sistema de paginação, etc. 
    url = 'https://api.github.com/repos/microsoft/vscode/pulls'
    # Neste exemplo, adicionei dois novos parâmetros. Leia a documentação dos pull requests 
    # para saber mais. 
    parameters = {'state': 'open', 'sort': 'updated', 'per_page': 10}
    next_page_available = True

    while(next_page_available):
        response = rest_request(url=url, parameters=parameters)
        pagination_urls = response.links

        open_pull_requests_in_current_page = response.json()

        for open_pull_request in open_pull_requests_in_current_page:
            print(open_pull_request['title'])

        if 'next' in pagination_urls:
            url = pagination_urls['next']['url']
        else:
            next_page_available = False  

example_one()
# example_two()
# example_three()
# example_four()
# example_five()

# Dúvidas? Sinta-se à vontade para me enviar um email 
# fronchettl@vcu.edu
