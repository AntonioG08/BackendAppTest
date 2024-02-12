from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompra(Resource):
    
    def get(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            return productocompra.to_json()
        except:
            return '', 404
        
    def delete(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
            return '', 201
        except:
            return '', 404
        
    def put(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(productocompra, key, value)
        try:
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json(), 201
        except:
            return '', 404
            


class ProductosCompras(Resource):
    
    def get(self):
        
        page = 1
        per_page = 5
        productoscompras = db.session.query(ProductoCompraModel)
        
        if request.get_json(silent=True): #silent = True means that we will ignore the fact that we wont receive Jsons always
            """In this part, we request the code to pay attention to any Json incoming. This way we can modify the value 
            of the variables 'page' and 'per_page'. Please check Insomnia for this"""
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)
                    
        productoscompras = productoscompras.paginate(page, per_page, True, 15)
        
        return jsonify({
            'productoscompras': [producto.to_json() for producto in productoscompras.items],
            'total': productoscompras.total,
            'pages': productoscompras.pages,
            'page': page
        })
        
    def post(self):
        productocompra = ProductoCompraModel.from_json(request.get_json())
        db.session.add(productocompra)
        db.session.commit()
        return productocompra.to_json(), 201
