import os
from flask import Flask
from dotenv import load_dotenv

# We import the module needed to create the api-rest
from flask_restful import Api

# We import now the module needed to be able to connect with an SQL DB
from flask_sqlalchemy import SQLAlchemy

# We import the module needed to work with JWT (Json Web Token)
from flask_jwt_extended import JWTManager

# We now import the module needed to work with the email
from flask_mail import Mail

"""We need to create an instance for the API"""
api = Api()

"""We need to create an instance now for SQLAlchemy"""
db = SQLAlchemy()

"""Now we instance the JWT"""
jwt = JWTManager()

"""Now we create the instance to work with the email"""
mailsender = Mail()


"""In this part we create the function 'create app' which we will be calling later in other scripts. We cant create this 
   function in the principal script due to 'flask' problems (investigate more about this), thats why it is created
   herer and then called in the other scripts to avoid problems"""
def create_app():
    
    app = Flask(__name__)
    
    # First we need to load the environment variables
    load_dotenv()
    
    # DB configuration
    path_db = os.getenv("Database_Path")
    db_name = os.getenv("Database_Name")
    """With this we are requesting to check if there is already a DataBase created with this name. In case it is not,
       the program will create one for the first time"""
    if not os.path.exists(f'{path_db}{db_name}'):
       os.chdir(f'{path_db}')
       file = os.open(f'{db_name}', os.O_CREAT)
      
    """In case there is currently a DataBase with this name, then the program will just connect us to it"""
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path_db}{db_name}'
    db.init_app(app)
   
    
    # First we import all the resources from the 'resources' script so we can use them
    import main.resources as resource
    """Check the application Insomina, there we can do quick tests to the server"""
    api.add_resource(resource.ClientesResource, '/clientes')
    api.add_resource(resource.ClienteResource, '/cliente/<id>')
    api.add_resource(resource.UsuariosResource, '/usuarios')
    api.add_resource(resource.UsuarioResource, '/usuario/<id>')
    api.add_resource(resource.ComprasResource, '/compras')
    api.add_resource(resource.CompraResource, '/compra/<id>')
    api.add_resource(resource.ProductosResource, '/productos')
    api.add_resource(resource.ProductoResource, '/producto/<id>')
    api.add_resource(resource.ProductosComprasResource, '/productos-compras')
    api.add_resource(resource.ProductoCompraResource, '/producto-compra/<id>')
    api.init_app(app)

   # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt.init_app(app)
   
   # Blueprints section
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import functions
    app.register_blueprint(mail.functions.mail)
    
   # Configurate email
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') 
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') 
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') 
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') 
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') 
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER') 
    
    mailsender.init_app(app)
    
    return app
    