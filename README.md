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

Por meio do método GET, podemos consultar dados de todos os funcionários no banco de dados:
    
    C:/PATH> curl http://127.0.0.1:5003/funcionarios/
    
    {"funcionarios": {"1": {"id": 1, "idade": 20, "nome": "Giovanni Amorim", "cargo": "Estagiario"}, "2": {"id": 2, "idade": 20, "nome": "Livinho", "cargo": "Diretor"}}}

ou dados de um funcionários específico, informando o seu id:

    C:/PATH> curl http://127.0.0.1:5003/funcionarios/1
    
    {"funcionario": {"id": 1, "idade": 20, "nome": "Giovanni Amorim", "cargo": "Estagiario"}}


# Adição de novos funcionários

Por meio do método POST, adicionamos novos funcionários à base de dados, informando sua idade, nome e cargo (o id é auto implementado):

    C:/PATH> curl -X POST -d "idade"="32" -d "nome"="'Lucas Silva'" -d "cargo"="'Analista'" http://127.0.0.1:5003/funcionarios/
    
    {"id": 3, "idade": 32, "nome": "Lucas Silva", "cargo": "Analista"}

siginifica que o funcionário foi adicionado com sucesso.
    
    
# Edição de dados de funcionários

Supondo que queremos mudar o cargo de um funcionário específico, podemos editar o valor nessa coluna deste funcionário na base de dados, por meio do método PUT:

    C:/PATH> curl -X PUT -d "dados"="id=3" -d "mudanca"="cargo='Diretor'" http://127.0.0.1:5003/funcionarios/
    
    "Dados de 1 funcionario(s) atualizados com sucesso."
    
significa que os antigos dados foram atualizados com sucesso.

Podemos também editar dados de funcionários baseando o request em mais de um dado, porém sempre editando apenas uma coluna por vez de cada funcionário ("mudanca"="idade=20 and cargo='Estagiario'" resultaria em uma confusão nos dados da tabela):

    C:/PATH> curl -X PUT -d "dados"="nome='Giovanni Amorim' and cargo='Estagiario'" -d "mudanca"="cargo='Analista'" http://127.0.0.1:5003/funcionarios/
    
    "Dados de 1 funcionario(s) atualizados com sucesso."
   
Claro que, não havendo compatibilidade entre os dados informados e algum funcionário existente, o retorno será:

    C:/PATH> curl -X PUT -d "dados"="id=1000" -d "mudanca"="idade=31" http://127.0.0.1:5003/funcionarios/
    
    "Dados de 0 funcionario(s) atualizados com sucesso."


# Remoção de dados de funcionários

Podemos remover os dados de um ou mais funcionários do banco de dados pelo método DELETE, onde informamos o 'filtro' da remoção como "dados":

    C:/PATH> curl -X DELETE -d "dados"="id=3" http://127.0.0.1:5003/funcionarios/

    "{'funcionarios removidos': {1: {'id': 3, 'idade': 32, 'nome': 'Lucas Silva', 'cargo': 'Diretor'}}}"


# Logs das ações

Na tabela "acoes" do banco de dados 'desafio.db', temos armazenadas todas as requisições que fizemos de maneira correta (e algumas mesmo de maneira incorreta).

A consulta a essa tabela é possível pelo seguinte endereço: 
    
    http://127.0.0.1:5003/logs/
    
E retorna o seguinte resutado (por exemplo):    

    {"acoes": 
      {"1": 
        {"id": 1, "metodo": "POST", "retorno": "{'id': 1, 'idade': 20, 'nome': 'Giovanni Amorim', 'cargo': 'Estagiario'}", "data_hora": "Tue, 14 Aug 2018 17:26:36 +0000"}, 
      "2":
        {"id": 2, "metodo": "POST", "retorno": "{'id': 2, 'idade': 20, 'nome': 'Livinho', 'cargo': 'Diretor'}", "data_hora": "Tue, 14 Aug 2018 17:26:40 +0000"}, 
      "3": 
        {"id": 3, "metodo": "GET", "retorno": "{'funcionarios': {1: {'id': 1, 'idade': 20, 'nome': 'Giovanni Amorim', 'cargo': 'Estagiario'}, 2: {'id': 2, 'idade': 20, 'nome': 'Livinho', 'cargo': 'Diretor'}}}", "data_hora": "Tue, 14 Aug 2018 17:26:44 +0000"},
      "4":
        {"id": 4, "metodo": "GET", "retorno": "{'funcionario': {'id': 1, 'idade': 20, 'nome': 'Giovanni Amorim', 'cargo': 'Estagiario'}}", "data_hora": "Tue, 14 Aug 2018 17:26:45 +0000"}, 
      "5":
        {"id": 5, "metodo": "POST", "retorno": "{'id': 3, 'idade': 32, 'nome': 'Lucas Silva', 'cargo': 'Analista'}", "data_hora": "Tue, 14 Aug 2018 17:26:57 +0000"},
      "6":
        {"id": 6, "metodo": "PUT", "retorno": "Dados de 1 funcionario(s) atualizados com sucesso.", "data_hora": "Tue, 14 Aug 2018 17:27:06 +0000"}, 
      "7":
        {"id": 7, "metodo": "PUT", "retorno": "Dados de 1 funcionario(s) atualizados com sucesso.", "data_hora": "Tue, 14 Aug 2018 17:27:20 +0000"},
      "8":
        {"id": 8, "metodo": "PUT", "retorno": "Dados de 0 funcionario(s) atualizados com sucesso.", "data_hora": "Tue, 14 Aug 2018 17:27:32 +0000"}, 
      "9":
        {"id": 9, "metodo": "DELETE", "retorno": "{'funcionarios removidos': {3: {'id': 3, 'idade': 32, 'nome': 'Lucas Silva', 'cargo': 'Diretor'}}}", "data_hora": "Tue, 14 Aug 2018 17:27:42 +0000"}}}










