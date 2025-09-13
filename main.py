#pip install flask_sqlalchemy
# Permite a conexão da API com o banco de dados
# flask permite a criaçao de API com Python
# Response e Request -> Requisiçao 

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask('vet')

# Rastreia modificações realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Configuração de conexão com banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_vet'

mybd = SQLAlchemy(app)

# Se refere a CLASSE que serve para definir o modelo dos dados que correspondem a tabela do banco de dados
class Vet(mybd.Model):
    __tablename__ = 'tb_veterinarios'
    id_veterinario = mybd.Column(mybd.Integer, primary_key = True)
    nome = mybd.Column(mybd.String(100))
    especialidade = mybd.Column(mybd.String(100))
    telefone = mybd.Column(mybd.String(100))
# Esse metodo to_json vai ser usado para converter o objeto em json
    def to_json(self):
        return{
            "id_veterinario": self.id_veterinario,
            "nome": self.nome,
            "especialidade": self.especialidade,
            "telefone": self.telefone
        }



# METODO 1 - GET (REALIZA UMA CONSULTA)
@app.route('/vet', methods = ['GET'])
def seleciona_carro():
    veterinario_selecionado = Vet.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_veterinarios)
    vet_json = [vet.to_json()
                for vet in veterinario_selecionado]
    return gera_resposta (200, vet_json)



# METODO GET (POR ID) - Como se fosse um WHERE 
@app.route('/vet/<id_veterinario_pam>', methods = ['GET'])
def seleciona_veterinario_id(id_veterinario_pam):
    veterinario_selecionado = Vet.query.filter_by(id_veterinario = id_veterinario_pam).first()
    vet_json = veterinario_selecionado.to_json()

    return gera_resposta(200, vet_json, 'Veterinario Encontrado!')

def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Lista de Veterinario'] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem 

    return Response(json.dumps(body), status=status, mimetype='application//json')    

app.run(port=5000, host='localhost', debug=True)


# METODO 3 - POST (ADICIONA UMA NOVA INFORMAÇAO)
@app.route('/vet', methods = ['POST'])
def criar_vet():
    requisicao = request.get_json()
    try:
        vet = Vet(
            id_veterinario = requisicao['id_veterinario'],
            nome = requisicao['nome'],
            especialidade = requisicao['especialidade'],
            telefone = requisicao ['telefone']
            )
        mybd.session.add(vet)
        mybd.session.commit()
        return gera_resposta(201, vet.to_json(), 'Criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400,{}, 'Erro ao cadastrar!')

# METODO 4 - DELETE 
@app.route('/vet/<id_veterinario_pam>', methods = ['DELETE'])
def deleta_veterinario(id_veterinario_pam):
    vet = Vet.query.filter_by(id_veterinario = id_veterinario_pam).first()

    try:
        mybd.session.delete(vet)
        mybd.session.commit()
        return gera_resposta(200, vet.to_json(), "Deletando com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao dele")

# METODO 5 - PUT (ATUALIZA UM VALOR)

@app.route('/vet/<id_veterinario_pam>', methods = ['PUT'])
def atualiza_vet(id_veterinario_pam):
    vet = Vet.query.filter_by(id_veterinario = id_veterinario_pam).first()
    requisicao = request.get_json()
    try:
        if ('nome' in requisicao):
            vet.nome = requisicao ['nome']
        if('especialidade' in requisicao):
            vet.especialidade = requisicao['ano']
        if ('telefone' in requisicao):
            vet.telefone = requisicao['valor']
        mybd.session.add(vet)
        mybd.session.commit()
        
        return gera_resposta(201, vet.to_json(), 'Criado com sucesso!') 
    
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400,{}, "Erro ao atualizar")

def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body['Lista de Carro'] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem 

    return Response(json.dumps(body), status=status, mimetype='application//json')    

app.run(port=5000, host='localhost', debug=True)

class Pet(mybd.Model):
    __tablename__ = 'tb_pets'
    id_pet = mybd.column(mybd.Integer, primary_key= True, autoincrement = True) 
    nome = mybd.column(mybd.String(100))
    tipo = mybd.column(mybd.String(100))
    raca = mybd.column(mybd.String(100))
    data_nascimento = mybd.column(mybd.String(100))
    id_cliente = mybd.column(mybd.Integer, mybd.ForeingKey('tb_clientes.id_cliente')), nullable = False

    def to_json(self):
        return{
        "id_pet": self.id_vet,
        "nome": self.nome,
        "tipo": self.tipo,
        "raca": self.raca,
        "data_nascimento": self.data_nascimento,
        "id_cliente": self.id_cliente
        }
# METODO 1 - GET - COMO SE FOSSE WHERE 
@app.route('/pets', methods = ['GET'])
def seleciona_pets():
    pet_selecionado = Pet.query.all()
    # Executa uma consulta no banco de dados (SELECT * FROM tb_veterinarios)
    pet_json = [pets.to_json()
                for pets in pet_selecionado]
    return gera_resposta (200, pet_json)

# METODO 2 - GET POR ID 
@app.route('/pets/<id_pet_pam>', methods = ['GET'])
def seleciona_pets_id(id_pet_pam):
    pet_selecionado = Pet.query.filter_by(id_pet = id_pet_pam).first()
    pets_json = pet_selecionado.to_json()

    return gera_resposta(200, pets_json, 'Veterinario Encontrado!')

def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Lista de Pets'] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem 

    return Response(json.dumps(body), status=status, mimetype='application//json') 

# METODO 3 - POST - ADICIONA UMA NOVA INFORMAÇÃO

@app.route('pets/', methods = ['POST'])
def criar_pet():
    requisicao = request.get_json()
    try:
        pets = Pet(
            id_pet = requisicao['id_pet'],
            nome = requisicao['nome'],
            tipo = requisicao['tipo'],
            raca = requisicao ['raca'],
            data_nascimento = requisicao['data_nascimento'],
            id_cliente = requisicao['id_cliente']
            )
        mybd.session.add(pets)
        mybd.session.commit()
        return gera_resposta(201, pets.to_json(), 'Criado com sucesso!')
    
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400,{}, 'Erro ao cadastrar!')
    
# METODO 4 - DELETE
@app.route('/pets/<id_pet_pam>', methods= ['DELETE'])
def deleta_pet(id_pet_pam):
    pets = Pet.query.filter_by(id_pet = id_pet_pam).first()

    try:
        mybd.session.delete(pets)
        mybd.session.commit()
        return gera_resposta(200, pets.to_json(), "Deletando com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, {}, "Erro ao dele")

# METODO 5 - PUT (ATUALIZA UM VALOR)

@app.route('/pets/<id_pet_pam>', methods = ['PUT'])
def atualiza_pet(id_pet_pam):
    pets = Pet.query.filter_by(id_pet = id_pet_pam).first()
    requisicao = request.get_json()
    try:
        if ('nome' in requisicao):
            pets.nome = requisicao ['nome']
        if('tipo' in requisicao):
            pets.tipo = requisicao['tipo']
        if ('raca' in requisicao):
            pets.raca = requisicao['ano']
        if ('data_nascimento' in requisicao):
            pets.data_nascimento = requisicao['data_nascimento']
        if('id_cliente' in requisicao):
            pets.id_cliente = requisicao['id_cliente']
        mybd.session.add(seleciona_pets_id)
        mybd.session.commit()
        
        return gera_resposta(201, pets.to_json(), 'Criado com sucesso!') 
    
    except Exception as e:
        print("Erro", e)
        return gera_resposta(400,{}, "Erro ao atualizar")