from flask import Blueprint
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

# _nomes = ['ESPETOS','CERVEJAS','BEBIDAS']
# _datas = [ data, data, data]

# doc = []
# for nome, adicionado_em in zip(_nomes, _datas):
#     doc.append({'nome':nome,'adicionado_em': adicionado_em})  

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

    categorySchema = {
        'nome': _nome,
        'adicionado_em':_data,
    }

    hasCategoryName = tb_categorias.find_one({'nome':_nome})
    if not hasCategoryName and request.method == 'POST':
        tb_categorias.insert_one(userSchema)
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
def put_categories():
    pass

@category.route('/api/category/delete/<id>', methods=['DELETE'])
def delete_categories():
    pass