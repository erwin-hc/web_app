from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def routes_links():
    div = ''' 
                <ul>
                <li><a target='_blank' href="/api/user/get">GET - Usuários</a></li>
                <li><a target='_blank' href="/api/custumer/get">GET - Clientes</a></li>
                <li><a target='_blank' href="/api/category/get">GET - Categorias</a></li>
                </ul>
          '''
    return div