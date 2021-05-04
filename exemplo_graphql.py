# O módulo requests abaixo é utilizado para fazermos as requisições HTTP
# Leia mais sobre este módulo em: https://docs.python-requests.org/
import requests

# Método que faz as requisições utilizando a API GraphQL (v4).
def graphql_request(query, headers = {}):
    # Repare que "query" aqui significa a requisição escrita em formato GraphQL, e headers
    # são cabeçalhos HTTP que podemos enviar a API ao realizar uma requisição.
    # Os cabeçalhos são importantes porque é através deles que realizamos a autenticação no GitHub,
    # assim como é através deles que requisitamos funcionalidades ainda em fase de testes à API (como é o caso do Discussions).
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    # Repare que em GraphQL nós enviamos uma requisição no formato GraphQL, mas a resposta que recebemos é JSON.
    # Se é JSON, basta utilizarmos dicionários do próprio Python para manipular as informações recebidas!
    return response.json()

# Aqui eu defino quais cabeçalhos HTTP eu vou passar pra minha requisição.
# Authorization é a chave que eu utilizo para autenticação com a API.
# GraphQL-Features é um valor customizado que eu utilizo pra pedir acesso ao recurso
# discussions da GitHub API que ainda está em fase de testes. Repare que a feature que eu estou
# solicitando é discussions_api (Leia mais em: https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions)

headers = {
    'Authorization': 'bearer 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',
    'GraphQL-Features': 'discussions_api'
}

# Finalmente a nossa query em formato GraphQL!
# Apesar dela se parecer com JSON, não é possível utilizar dicionários Python para
# representar uma query em GraphQL. Por isso, eu coloco tudo dentro de uma string.
# Uma alternativa seria usar o GraphQL explorer pra testar sua query em GraphQL, e depois
# só colar o que tu montou lá aqui dentro de uma string (Veja mais em: https://docs.github.com/en/graphql/overview/explorer). 

query = """
{
    repository(name: "next.js", owner:"vercel") {
        discussions(first: 10) {
            edges {
                node {
                    title
                    author {
                        login
                    }
                    answerChosenAt
                }
            }
        }
    }
}
"""

# Repare que na requisição acima eu estou solicitando informações do projeto next.js, da organização vercel.
# Em GraphQL nós temos que definir quais informações desejamos receber. No exemplo acima eu estou solicitando 
# o título da discussion, o login do autor dela, e quando a resposta foi escolhida.
# Pra saber exatamente o que tu pode coletar, visite a API em: https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions#discussion

# Realizo a requisição passando a query e os cabeçalhos
json = graphql_request(query, headers)
# Imprimo o resultado
print(json)