from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from time import localtime, strftime
import sqlite3

database_name="desafio.db"
db_connect = create_engine('sqlite:///{}'.format(database_name))
app = Flask(__name__)
api = Api(app)

class Inicio(Resource):
    def get(self):
        retorno = "Banco de dados de funcionarios."


class Funcionarios(Resource):
    def get(self): # curl http://127.0.0.1:5003/funcionarios/
        conn = db_connect.connect()
        query = conn.execute("select * from funcionarios")
        result = {'funcionarios' : {i[0]: dict(zip(tuple(query.keys()), i)) for i in query.cursor}}
        conn.execute("""insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('GET',str(result),strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
        return result


    def post(self): # curl -X POST -d "idade"="24" -d "nome"="'Vitoria'" -d "cargo"="'Analista'" http://127.0.0.1:5003/funcionarios/
        try:
            idade = request.form.get('idade')
            nome = request.form.get('nome')
            cargo = request.form.get('cargo')
            conn = sqlite3.connect(database_name)
            c = conn.cursor()
            c.execute("insert into funcionarios (idade,nome,cargo) values ({})".format(idade+", "+nome+", "+cargo))
            for row in c.execute("select * from funcionarios where idade={} and nome={} and cargo={}".format(idade,nome,cargo)):
                retorno = dict(zip(('id','idade','nome','cargo'),row))
            #c.execute("""insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('POST',str(retorno),strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
            #conn.commit()
            #conn.close()
        except Exception as e:
            retorno = {
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            }
        c.execute("""insert into acoes (metodo, retorno, data_hora) values ("{}","{}","{}")""".format('POST',str(retorno),strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
        conn.commit()
        conn.close()
        return retorno



    def put(self): # curl -X PUT -d "dados"="idade=24 and nome='Vitoria'" -d "mudanca"="idade=25" http://127.0.0.1:5003/funcionarios/
        try:
            dados = request.form.get('dados')
            mudanca = request.form.get('mudanca')
            conn = sqlite3.connect(database_name)
            c = conn.cursor()
            c.execute("update funcionarios set {} where {}".format(mudanca,dados))
            retorno = "(antigos_dados:{},novos_dados:{})".format(dados,mudanca)
            #c.execute("""insert into acoes (metodo, retorno, data_hora)  values ("{}","(antigos_dados:{},novos_dados:{})","{}")""".format('PUT',dados,mudanca,strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
            #conn.commit()
            #conn.close()
        except Exception as e:
            retorno = {
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            }
        if type(retorno) is str:
            c.execute("""insert into acoes (metodo, retorno, data_hora)  values ("{}","(antigos_dados:{},novos_dados:{})","{}")""".format('PUT', dados, mudanca, strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
        else:
            c.execute("""insert into acoes (metodo, retorno, data_hora)  values ("{}","{}","{}")""".format('PUT', str(retorno), strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
        conn.commit()
        conn.close()
        return retorno

    def delete(self): # curl -X DELETE -d "dados"="idade=25" http://127.0.0.1:5003/funcionarios/
        try:
            dados = request.form.get('dados')
            conn = sqlite3.connect(database_name)
            c = conn.cursor()
            c.execute("delete from funcionarios where {}".format(dados))
            #c.execute("""insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('DELETE',"filtro: "+ str(dados),strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
            #conn.commit()
            #conn.close()
            retorno = "filtro: "+ str(dados)
        except Exception as e:
            retorno = {
                'mensagem': 'Ocorreu um erro',
                'erro': str(e)
            }
        if type(retorno) is str:
            c.execute("""insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('DELETE',"filtro: " + str(dados),strftime("%a, %d %b %Y %H:%M:%S +0000",localtime())))
        else:
            c.execute("""insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('DELETE',str(retorno),strftime("%a, %d %b %Y %H:%M:%S +0000",localtime())))
        conn.commit()
        conn.close()
        return retorno


class Funcionario_ID(Resource):
    def get(self, id_funcionario): # curl http://127.0.0.1:5003/funcionarios/1
        conn = db_connect.connect()
        query = conn.execute("select * from funcionarios where id =%d " % int(id_funcionario))
        result = {'funcionario' : dict(zip(tuple(query.keys()), i)) for i in query.cursor}
        conn.execute("""insert into acoes (metodo,retorno,data_hora) values ("{}","{}","{}")""".format('GET',str(result),strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
        return result

class Logs(Resource):
    def get(self): # curl http://127.0.0.1:5003/logs/
        conn = db_connect.connect()
        query = conn.execute("select * from acoes")
        result = {'acoes' : {i[0]: dict(zip(tuple(query.keys()), i)) for i in query.cursor}}
        return result

api.add_resource(Inicio,'/')
api.add_resource(Funcionarios, '/funcionarios/',methods=['GET','POST','PUT','DELETE'])
api.add_resource(Funcionario_ID, '/funcionarios/<id_funcionario>')
api.add_resource(Logs,'/logs/')


if __name__ == '__main__':
    app.run(port='5003')