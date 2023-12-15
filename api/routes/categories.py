from flask import Blueprint, request, Response
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

category = Blueprint('category', __name__)
@category.route('/api/category/get', methods=['GET'])
def get_categories():
    tb_categorias = mongo.db['TB_CATEGORIAS']
    # tb_categorias.insert_many(doc)

    agrr = tb_categorias.aggregate([
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
            "usuario_id": { "$toString": "$_id" },
            "USUARIO": { "$map": { "input": "$USUARIO", 'in': { "_id": { "$toString": '$$this._id'}, "nome":"$$this.nome" }}}   
        }   
    },
    {
        "$project": {"usuario_id":0}
    }
    ])
    
    dados = []
    for item in agrr:
        dados.append(item) 
    return dados

@category.route('/api/category/post', methods=['POST'])
def post_categories():
    tb_categorias = mongo.db['TB_CATEGORIAS']

    _nome = request.get_json()['nome']
    _adicionado_em = data
    _usuario_id = request.get_json()['usuario_id']

    categorySchema = {
        'nome': _nome,
        'adicionado_em':_adicionado_em,
        'usuario_id': ObjectId(_usuario_id)
    }

    hasCategoryName = tb_categorias.find_one({'nome':_nome})
    if not hasCategoryName and request.method == 'POST':
        tb_categorias.insert_one(categorySchema)
        return Response(
            response = json.dumps('CATEGORIA RECEBIDA!'),
            status = 200,
            mimetype = "application/json"
            )
    else:        
        return Response(
            response = json.dumps('ERRO! CATEGORIA JA EXISTE NO BANCO'),
            status = 500,
            mimetype = "application/json"
        )

@category.route('/api/category/put/<id>', methods=['PUT'])
def put_categories(id):
    tb_categorias = mongo.db['TB_CATEGORIAS']

    _nome = request.get_json()['nome']
    _adicionado_em = data
    _usuario_id = request.get_json()['usuario_id']

    categorySchema = { '$set': { 
        'nome': _nome,
        'adicionado_em':_adicionado_em,
        'usuario_id': ObjectId(_usuario_id)
    }}

    hasCategoryID = tb_categorias.find_one({'_id': ObjectId(id)})
    if hasCategoryID:
        filtro = { "_id" : hasCategoryID['_id'] }
        tb_categorias.update_one(filtro, categorySchema)
        return Response(
            response = json.dumps('CATEGORIA ALTERADA!'),
            status = 200,
            mimetype = "application/json"
            )
    else:        
        return Response(
            response = json.dumps('ERRO! CATEGORIA NAO EXISTE NO BANCO'),
            status = 500,
            mimetype = "application/json"
        )

@category.route('/api/category/delete/<id>', methods=['DELETE'])
def delete_categories(id):
    tb_categorias = mongo.db['TB_CATEGORIAS']

    hasCategoryID = tb_categorias.find_one({'_id': ObjectId(id)})
    if hasCategoryID:
        filtro = { "_id" : hasCategoryID['_id'] }
        tb_categorias.delete_one(filtro)
        return Response(
            response = json.dumps('CATEGORIA DELETADA!'),
            status = 200,
            mimetype = "application/json"
            )
    else:        
        return Response(
            response = json.dumps('ERRO! CATEGORIA NAO EXISTE NO BANCO'),
            status = 500,
            mimetype = "application/json"
        )