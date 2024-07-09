# API de Gestão de Ativos

## Descrição

Esta é uma API RESTful desenvolvida com Flask para a gestão de ativos financeiros. A API permite criar, listar, obter, atualizar e deletar ativos financeiros. Além disso, a API permite obter a lista de símbolos de ativos e os valores atuais dos ativos utilizando a API AlphaVantage.

## Funcionalidades

- **GET /ativos**: Obter a lista de ativos.
- **GET /ativos/{id}**: Obter um ativo específico.
- **POST /ativos**: Inserir um novo ativo.
- **PUT /ativos/{id}**: Alterar a quantidade de um ativo.
- **DELETE /ativos/{id}**: Deletar um ativo.
- **GET /ativos/symbols**: Obter a lista de símbolos de ativos.

## Tecnologias Utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flasgger
- SQLite
- Docker

## Pré-requisitos

- Docker instalado

## Configuração e Execução

1. Clone o repositório para sua máquina local:
    ```sh
    git clone https://github.com/FelipyPenhaBotega/MVP_gestao_ativos_backend.git
    cd MVP_gestao_ativos_backend
    ```

2. Obtenha a sua chave da API AlphaVantage, necessária para configurar a variável de ambiente `ALPHA_VANTAGE_API_KEY`, em: https://www.alphavantage.co/support/#api-key

3. Construa a imagem Docker:
    ```sh
    docker build -t backend .
    ```

4. Execute o contêiner Docker:
    ```sh
    docker run -e ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY -p 5000:5000 backend
    ```

5. Acesse a documentação Swagger da API em:
    ```
    http://localhost:5000/apidocs/#/
    ```

## Exemplos de Requisições

### Obter a Lista de Ativos

```sh
curl -X GET http://localhost:5000/ativos
