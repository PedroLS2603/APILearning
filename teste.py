from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Instanciando o arquivo
app = Flask(__name__)

#Importando as configurações da aplicação de um arquivo externo
app.config.from_pyfile('config.cfg')

#Instanciando SQLAlchemy e Marshmallow
db = SQLAlchemy(app)    
ma = Marshmallow(app)

#Criando tabelas no banco de dados
class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(20))
    nasc = db.Column(db.Date)
    cpf = db.Column(db.String(14))
    def __init__(self, nome, nasc, cpf):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf

#Criando os schemas das tabelas

class TestSchema(ma.Schema):
    class Meta:
        fields = ('id','nome','nasc','cpf')

#Iniciando os schemas das tabelas
test_schema = TestSchema()
mtest_schema = TestSchema(many=True)

#Cria no banco de dados alguma alteração feita no arquivo Model.py
db.create_all()
db.session.commit()

#Rotas e suas funcionalidades
@app.route('/')
def index():
    all_tests = Test.query.all()
    result = mtest_schema.dump(all_tests)
    return jsonify(result) 

#Cria um novo objeto teste no banco de dados
@app.route('/test', methods=['POST'])
def add_test():
    nome = request.json['nome']
    nasc = request.json['nasc']
    cpf = request.json['cpf']

    new_test = Test(nome,nasc,cpf)

    db.session.add(new_test)
    db.session.commit()
    return test_schema.jsonify(new_test)

#Pega todos os objetos teste no banco de dados
@app.route('/testes', methods=['GET'])
def get_tests():
    all_tests = Test.query.all()
    result = mtest_schema.dump(all_tests)
    return jsonify(result)

#Pega um único objeto teste no banco de dados pelo ID
@app.route('/test/<id>', methods=['GET'])
def get_test(id):
    test = Test.query.get(id)
    return test_schema.jsonify(test)

#Altera as informações de um objeto teste já existente no banco de dados
@app.route('/test/<id>', methods=['PUT'])
def update_test(id):
    test = Test.query.get(id)

    nome = request.json['nome']
    nasc = request.json['nasc']
    cpf = request.json['cpf']

    test.nome = nome
    test.nasc = nasc
    test.cpf = cpf

    db.session.commit()
    return test_schema.jsonify(test)

#Deleta um único objeto teste no banco de dados pelo ID
@app.route('/test/<id>', methods=['DELETE'])
def delete_test(id):
    test = Test.query.get(id)
    db.session.delete(test)
    db.session.commit()
    return test_schema.jsonify(test)

#roda o app
if __name__ == '__main__':
    app.run()
