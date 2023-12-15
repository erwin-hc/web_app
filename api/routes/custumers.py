from flask import Blueprint, Response, request
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

custumer = Blueprint('custumer', __name__)
@custumer.route('/api/custumer/get', methods=['GET'])
def get_custumer():
    tb_clientes = mongo.db['TB_CLIENTES']
    agrr = tb_clientes.aggregate([
    {     
        "$lookup":
        {
            "from": "TB_USUARIOS",
            "localField": "usuario_id",
            "foreignField": "_id",
            "as": "USUARIO",                        
        }  
    },
    {     
            "$addFields":
            { 
            "_id": { "$toString": "$_id" },
            "usuario_id": { "$toString": "$usuario_id"},
            "USUARIO": { "$map": { "input": "$USUARIO", 'in': { "_id": { "$toString": '$$this._id'}, "nome":"$$this.nome" }}}
            }  
    },
    # {
    #     "$project":
    #     {
    #         "usuario_id":0
    #     }
    # }
    ])

    dados = []
    for item in agrr:
        dados.append(item) 
    return dados

@custumer.route('/api/custumer/post', methods=['POST'])
def post_custumer():
    tb_clientes = mongo.db['TB_CLIENTES']

    _nome = request.get_json()['nome']
    _fone = request.get_json()['fone']
    _usuario_id = request.get_json()['usuario_id']
    _adicionado_em = data

    custumerSchema = {
        'nome': _nome,
        'fone': _fone,
        'adicionado_em':_adicionado_em,
        'usuario_id': ObjectId(_usuario_id)
    }

    hasCustumerFone = tb_clientes.find_one({'fone':_fone})
    if not hasCustumerFone and request.method == 'POST':
        tb_clientes.insert_one(custumerSchema)
        return Response(
            response = json.dumps('CLIENTE RECEBIDO!'),
            status = 200,
            mimetype = "application/json"
            )
    else:        
        return Response(
            response = json.dumps('ERRO! TELEFONE JA EXISTE NO BANCO'),
            status = 500,
            mimetype = "application/json"
        )

@custumer.route('/api/custumer/put/<id>')
def put_custumer(id):
    pass

@custumer.route('/api/custumer/delete/<id>')
def delete_custumer(id):
    pass