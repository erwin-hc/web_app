from flask import Blueprint, request, Response
import json
from datetime import datetime
from bson import ObjectId

data = datetime.now().strftime('%d-%m-%Y')

from ..extensions import mongo

_nome = '100-G'
_data =  data
_categoria_id = "657c8aa23a6b3b8386d5d16b"
_usuario_id = '6570b310481886e4bd551668'

sizeSchema = {
    "nome":_nome,
    "adicionado_em":_data,
    "categoria_id":_categoria_id,
    "usuario_id":_usuario_id 
}


size = Blueprint('size', __name__)
@size.route('/api/sizes/get', methods=['GET'])
def get_sizes():
    pass

@size.route('/api/sizes/post', methods=['POST'])
def post_sizes():
    pass

@size.route('/api/sizes/put', methods=['PUT'])
def put_sizes(id):
    pass

@size.route('/api/sizes/delete', methods=['DELETE'])
def delete_sizes(id):
    pass