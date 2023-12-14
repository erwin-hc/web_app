from flask import Blueprint, Response, request
from werkzeug.security import generate_password_hash
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')


from ..extensions import mongo

user = Blueprint('user', __name__)

@user.route('/api/user/get', methods=['GET'])
def get_user(): 
    tb_usuarios = mongo.db['TB_USUARIOS']
    agrr = tb_usuarios.aggregate([
    {     
        "$addFields":
        { 
            "_id": { "$toString": "$_id" },
        }   
    }
    ])

    dados = []
    for item in agrr:
        dados.append(item) 
    return dados

@user.route('/api/user/post', methods=['POST'])
def post_user():
    tb_usuarios = mongo.db['TB_USUARIOS']

    _nome = request.get_json()['nome']
    _senha = generate_password_hash(request.get_json()['senha'])
    _email = request.get_json()['email']
    _data = data

    userSchema = {
        'nome': _nome,
        'senha': generate_password_hash(_senha),
        'adicionado_em':_data,
        'email': _email
    }

    hasUser = tb_usuarios.find_one({'email':_email})
    if not hasUser and request.method == 'POST':
        tb_usuarios.insert_one(userSchema)
        return Response(
            response = json.dumps('USUARIO RECEBIDO!'),
            status = 200,
            mimetype = "application/json"
            )
    else:        
        return Response(
            response = json.dumps('ERRO! EMAIL JA EXISTE NO BANCO'),
            status = 500,
            mimetype = "application/json"
        )

@user.route('/api/user/put/<id>', methods=['PUT'])
def user_put(id):
    tb_usuarios = mongo.db['TB_USUARIOS']

    _nome = request.get_json()['nome']
    _senha = generate_password_hash(request.get_json()['senha'])
    _email = request.get_json()['email']
    _data = data

    userSchema = { "$set": {
        'nome': _nome,
        'senha': generate_password_hash(_senha),
        'adicionado_em':_data,
        'email': _email
    }}

    hasID = tb_usuarios.find_one({'_id': ObjectId(id)})
    if not hasID:
        return Response(
            response = json.dumps('ERRO! USUARIO NAO ENCONTRADO'),
            status = 500,
            mimetype = "application/json"
        )
    else:
        filtro = { "_id" : hasID['_id'] }
        tb_usuarios.update_one(filtro, userSchema)
        return Response(
            response = json.dumps('USUARIO ATUALIZADO'),
            status = 200,
            mimetype = "application/json"
        )

@user.route('/api/user/delete/<id>', methods=['DELETE'])
def user_delete(id):
    tb_usuarios = mongo.db['TB_USUARIOS']

    hasID = tb_usuarios.find_one({'_id': ObjectId(id)})
    if not hasID:
        return Response(
            response = json.dumps('ERRO! USUARIO NAO ENCONTRADO'),
            status = 500,
            mimetype = "application/json"
        )
    else:
        filtro = { "_id" : hasID['_id'] }
        tb_usuarios.delete_one(filtro)
        return Response(
            response = json.dumps('USUARIO EXCLUIDO'),
            status = 200,
            mimetype = "application/json"
        )
