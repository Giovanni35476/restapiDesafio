from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from time import localtime, strftime

database_name = "desafio.db"
db_connect = create_engine('sqlite:///{}'.format(database_name))
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)


class Inicio(Resource):
    def get(self):
        return "Bem vindo ao banco de dados de funcionarios."


class Funcionarios(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from funcionarios")
        result = {'funcionarios': {i[0]: dict(zip(tuple(query.keys()), i)) for i in query.cursor}}
        conn.execute(
            """insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('GET', str(result),
                                                                                                strftime(
                                                                                                    "%a, %d %b %Y %H:%M:%S +0000",
                                                                                                    localtime())))
        return jsonify(result)

    def post(self):
        try:
            conn = db_connect.connect()
            idade = request.form.get('idade')
            nome = request.form.get('nome')
            cargo = request.form.get('cargo')
            conn.execute("insert into funcionarios (idade,nome,cargo) values ({})".format(idade + ", " + nome + ", " + cargo))
            query = conn.execute("select * from funcionarios where id=(select max(id) from funcionarios)")
            return jsonify([dict(zip(tuple(query.keys()), i)) for i in query.cursor][0])
        except Exception as e:
            retorno = jsonify({
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            })
            retorno.status_code = 400
        conn.execute(
            """insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('POST', str(retorno),
                                                                                                strftime(
                                                                                                    "%a, %d %b %Y %H:%M:%S +0000",
                                                                                                    localtime())))
        return retorno

    def put(self):
        try:
            conn = db_connect.connect()
            dados = request.form.get('dados')
            mudanca = request.form.get('mudanca')
            contador = 0
            query = conn.execute("select * from funcionarios where {}".format(dados))
            for row in query.cursor:
                contador += 1
            conn.execute("update funcionarios set {} where {}".format(mudanca, dados))
            retorno = "Dados de {} funcionario(s) atualizados com sucesso.".format(contador)
        except Exception as e:
            retorno = jsonify({
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            })
            retorno.status_code = 400
        conn.execute(
            """insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('PUT', str(retorno),
                                                                                                strftime(
                                                                                                    "%a, %d %b %Y %H:%M:%S +0000",
                                                                                                    localtime())))
        return retorno

    def delete(self):
        try:
            conn = db_connect.connect()
            dados = request.form.get('dados')
            query = conn.execute("select * from funcionarios where {}".format(dados))
            result = {'funcionario(s) removido(s)': {i[0]: dict(zip(tuple(query.keys()), i)) for i in query.cursor}}
            conn.execute("delete from funcionarios where {}".format(dados))
            retorno = result
        except Exception as e:
            retorno = {
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            }
            retorno.status_code = 400
        conn.execute(
            """insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('DELETE', str(retorno),
                                                                                              strftime(
                                                                                                  "%a, %d %b %Y %H:%M:%S +0000",
                                                                                                  localtime())))
        return jsonify(retorno)


class Funcionario_ID(Resource):
    def get(self, id_funcionario):
        conn = db_connect.connect()
        query = conn.execute("select * from funcionarios where id =%d " % int(id_funcionario))
        result = {'funcionario': dict(zip(tuple(query.keys()), i)) for i in query.cursor}
        conn.execute(
            """insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('GET', str(result),
                                                                                              strftime(
                                                                                                  "%a, %d %b %Y %H:%M:%S +0000",
                                                                                                  localtime())))
        return jsonify(result)


class Logs(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from acoes")
        result = {'acoes': {i[0]: dict(zip(tuple(query.keys()), i)) for i in query.cursor}}
        return jsonify(result)


api.add_resource(Inicio, '/')
api.add_resource(Funcionarios, '/funcionarios/', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(Funcionario_ID, '/funcionarios/<id_funcionario>')
api.add_resource(Logs, '/logs/')

if __name__ == '__main__':
    app.run(port=5003)
