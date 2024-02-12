from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel
from main.auth.decorators import role_required

class Producto(Resource):
    
    """With this function we can get the information contained in an specific ID of the DataBase"""
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        # SELECT * FROM producto WHERE producto.id = 1
        try:
            return producto.to_json()
        except:
            return 'Resource not found', 404
    
    """With this function we are able to modify a DataBase register, we can pass all the parameters, or only the one we 
    want to change"""
    @role_required(roles=['admin'])
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            """The set attribute method needs 3 parameters, the object name, the key and the value. Please note that
               dictionaries uses keys and values to store its content"""
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except:
            return '', 404
    
    """With this function we can delete an specific record from the DataBase"""
    @role_required(roles=['admin'])
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.commit()
        except:
            return '', 404


class Productos(Resource):
    
    def get(self):
        page = 1
        per_page = 5
        """This command was used in the past to bring all the products from the DataBase, but now we only bring back 5 at
        the time 
        productos = db.session.query(ProductoModel).all()
        # SELECT * FROM producto
        return jsonify({
            'productos' : [producto.to_json() for producto in productos]
        }) """
        productos = db.session.query(ProductoModel)
        
        if request.get_json(silent=True): #silent = True means that we will ignore the fact that we wont receive Jsons always
            """In this part, we request the code to pay attention to any Json incoming. This way we can modify the value 
            of the variables 'page' and 'per_page'. Please check Insomnia for this"""
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
        
        productos = productos.paginate(page, per_page, True, 15)
        
        return jsonify({
            'productos': [producto.to_json() for producto in productos.items],
            'total': productos.total,
            'pages': productos.pages,
            'page': page
        })
    
    # Function used to add products to our DataBase hosted in SQLite3
    @role_required(roles=['admin'])
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201
    