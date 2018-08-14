# restapiDesafio

Para começar, deve-se ter instaladas as seguintes bibliotecas:

flask: https://github.com/pallets/flask

flask_restful : https://github.com/flask-restful/flask-restful

sqlalchemy : https://github.com/zzzeek/sqlalchemy/


# Base de dados

O arquivo "db_config.py" gera a base de dados chamada "desafio.db" e, em seguida, cria as tabelas "funcionarios" e "acoes".

Na tabela "funcionarios", salvaremos todos os dados dos funcionários adicionados.
Nela temos as colunas: 
  "id", que é auto implementada por um número inteiro;
  "idade", também inteiro;
  e as duas colunas com dados em texto, que são "nome" e "cargo".

Na tabela "acoes" teremos salvas todas as ações que requisitarmos à base de dados.
As colunas são: 
  "id", também auto implementada por inteiro; 
  "metodo", que pode ser "GET", "POST", "PUT" ou "DELETE";
  "retorno", que salva o que a requisição recebeu como retorno, sendo em forma de dados da tabela, mensagens de texto ou até mensagens de erro;
  "data_hora", sendo o horário regional da requisição.


# Consulta aos dados de funcionários

Por meio do método GET podemos consultar dados de todos os funcionários no banco de dados:
    
    C:/PATH> curl http://127.0.0.1:5003/funcionarios/
    
    {"funcionarios": {"1": {"id": 1, "idade": 19, "nome": "Giovanni", "cargo": "Estagiario"}, "2": {"id": 2, "idade": 20, "nome": "Livinho", "cargo": "Diretor"}}}

ou dados de um funcionários específico, informando o seu id:

    C:/PATH> curl http://127.0.0.1:5003/funcionarios/1
    
    {"funcionario": {"id": 1, "idade": 19, "nome": "Giovanni", "cargo": "Estagiario"}}
