from flask_restful import Resource
from flask import jsonify, request
from .. import db
from main.models import UsuarioModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity


"""At the beginning we are not using a real DataBase for the project, therefore we are simulating a Database using a 
   list with dictionaries inside, which are basically Json objects"""

      
class Cliente_ind(Resource):
    
    @role_required(roles=["admin", "cliente"])
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        
        if cliente.role == 'cliente':
            if current_user['usuarioId'] == cliente.id or current_user['role'] =='admin':
                return cliente.to_json()
            else:
                return 'Unauthorized', 401
        else:
            return 'You are not a client', 404
        
    @role_required(roles=["admin", "cliente"])
    def delete(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        
        # Section where the current user or an admin can delete users
        if current_user['usuarioId'] == cliente.id or current_user['role'] == 'admin':
            
            # Section for deleting clients
            if cliente.role == 'cliente':
                try:
                    db.session.delete(cliente)
                    db.session.commit()
                    return 'User deleted', 204
                except:
                    return 'Error, could not delete the user', 404
                
            # Section for deleting admins, note that only an admin can delete an admin    
            elif cliente.role == 'admin' and current_user['role'] == 'admin':
                try:
                    db.session.delete(cliente)
                    db.session.commit()
                    return 'User deleted', 204
                except:
                    return 'Error, could not delete the user', 404
            else:
                return 'Error, could not delete the user', 404
        else:
            return 'Unauthorized', 401
            
    @role_required(roles=["cliente"])
    def put(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente' and current_user['usuarioId'] == cliente.id:
            data = request.get_json().items()
            for key, value in data:
                setattr(cliente, key, value)
            try:
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(), 201
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        
        
class Clientes(Resource):
    
    """When programming 'HTML' we have basically 4 methods we can use, we can use the 'GET' method wich pulls information 
       from the API, the 'POST' method which will push or public information to the API, the 'DELETE' to erase a resource
       from the API, and 'PUT' method to edit a resource from the API."""

    # With the decorator below us, only an admin can see the list of 'clientes'
    """For the server to know that we are admins, we need to login in through auth, and once we log in we need to enter the 
       given token in the section 'bearer' of Insomnia. Please remember that we set that the token is only valid for 
       3600 seconds, or 1 hour."""
    
    """If we attempt to enter the token, but from a logged user that is a 'client' and not an 'admin', the system will not 
       allow this and will return an error along with the message 'Rol not allowed' """
    @role_required(roles=["admin"])
    def get(self):
        
        page = 1
        per_page = 5
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')
        
        if request.get_json(silent=True): 
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        
        clientes = clientes.paginate(page, per_page, True, 10)
        
        return jsonify({
            'clientes': [cliente.to_json() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'page': page
        })
        
    """Please NOTE that if we attempt to create a user or customer with an already existing email, it will throw us 
       an error back because we cant use the same email twice"""
    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.role == 'cliente'
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201
