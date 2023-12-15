from flask import Blueprint, Response, request
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

custumer = Blueprint('custumer', __name__)
@custumer.route('/api/custumer/get')
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
    {
        "$project":
        {
            "usuario_id":0
        }
    }
    ])

    dados = []
    for item in agrr:
        dados.append(item) 
    return dados

@custumer.route('/api/custumer/post')
def post_custumer():
    pass

@custumer.route('/api/custumer/put/<id>')
def put_custumer(id):
    pass

@custumer.route('/api/custumer/delete/<id>')
def delete_custumer(id):
    pass