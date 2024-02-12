from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel


class Usuario(Resource):
    
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201

    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.commit()
        return '', 404


class Usuarios(Resource):
    
    def get(self):
        
        page = 1
        per_page = 5
        usuarios = db.session.query(UsuarioModel)
        
        if request.get_json(silent=True): #silent = True means that we will ignore the fact that we wont receive Jsons always
            """In this part, we request the code to pay attention to any Json incoming. This way we can modify the value 
            of the variables 'page' and 'per_page'. Please check Insomnia for this"""
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
                    
        usuarios = usuarios.paginate(page, per_page, True, 15)
        
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'page': page
        })
        