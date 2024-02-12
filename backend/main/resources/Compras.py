from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity

class Compra(Resource):
        
    """With this function we can get the information contained in an specific ID of the DataBase"""
    @role_required(roles=['admin', 'cliente'])
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == "admin":
            try:
                return compra.to_json()
            except:
                return 'Resource not found', 404
        else:
            return 'Unauthorized', 401
    
    
    """With this function we are able to modify a DataBase register, we can pass all the parameters, or only the one we 
    want to change"""
    @role_required(roles=['admin', 'cliente'])
    def put(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == 'admin':
            data = request.get_json().items()
            for key, value in data:
                """The set attribute method needs 3 parameters, the object name, the key and the value. Please note that
                dictionaries uses keys and values to store its content"""
                setattr(compra, key, value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
    
    
    """With this function we can delete an specific record from the DataBase"""
    @role_required(roles=['admin', 'cliente'])
    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == 'admin':
            try:
                db.session.delete(compra)
                db.commit()
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        

class Compras(Resource):
    
    @role_required(roles=['admin'])
    def get(self):
        page = 1
        per_page = 5
        compras = db.session.query(CompraModel)
        
        """Its very important this 'if' because meaybe the user does not wants to specify the page or de number of items
           per page, and the code needs to keep running. The 'silent=True' is telling the code that not always the user 
           will send a Json with information, and that it needs to keep running eventhough."""
        if request.get_json(silent=True): 
            """In this part, we request the code to pay attention to any Json incoming. This way we can modify the value 
            of the variables 'page' and 'per_page'. Please check Insomnia for this"""
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        
        compras = compras.paginate(page, per_page, True, 15)
        
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items],
            'total': compras.total,
            'pages': compras.pages,
            'page': page
        })
        
    @role_required(roles=['admin', 'cliente'])    
    def post(self):
        compra = CompraModel.from_json(request.get_json())
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201