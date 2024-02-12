from flask import request, Blueprint
from main.models.Usuario import Usuario
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identity_lookup
from main.mail.functions import send_mail

"""Here we will have all the information regarding the routes for the user to log in or to create an account"""

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    # First we search for the user in the DB using his/her registered email
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first_or_404()
    
    # Now we validate that the password of the user is correct
    if usuario.validate_password(request.get_json().get('password')):
        # We generate a token and set the user as that token´s identity
        # Here we need to have imported the 'user_identity_lookup from main auth decorators. Failure to will break the code
        access_token = create_access_token(identity=usuario)
        """Note: The access web token is like a temporarily password or key, currently we set it to be functional for 3600 
           seconds. This could normally be stored in the 'cookied' of the server, as it will be restarted or change its 
           value once the user logs again"""
        data = {
            'id': str(usuario.id),
            'email': str(usuario.email),
            'access_token': access_token,
            'role': str(usuario.role)
        }
        return data, 200
    
    else:
        return 'Incorret password', 401
        

@auth.route('/register', methods=['POST'])
def register():
    usuario = UsuarioModel.from_json(request.get_json())
    exist = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
    if exist:
        return 'Duplicated email', 409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()
            send_mail([usuario.email], "Bienvenido a nuestra app", 'register', usuario=usuario)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json(), 201
