from flask import Blueprint
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

# _nomes = ['ESPETOS','CERVEJAS','BEBIDAS']
# _tamanhos = [['150-G','200-G ','250-G'],['350-ML','475-ML ','600-ML'],['350-ML','600-ML ','1.0-L']]
# _datas = [ data, data, data]

# doc = []
# for nome, tamanho, adicionado_em in zip(_nomes, _tamanhos, _datas):
#     doc.append({'nome':nome, 'tamanho':tamanho, 'adicionado_em': adicionado_em})  

category = Blueprint('category', __name__)
@category.route('/api/category/get', methods=['GET'])
def get_categories():
    tb_categorias = mongo.db['TB_CATEGORIAS']
    # tb_categorias.insert_many(doc)

    agrr = tb_categorias.aggregate([
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

@category.route('/api/category/post', methods=['POST'])
def post_categories():
    pass



@category.route('/api/category/put/<id>', methods=['PUT'])
def put_categories():
    pass

@category.route('/api/category/delete/<id>', methods=['DELETE'])
def delete_categories():
    pass