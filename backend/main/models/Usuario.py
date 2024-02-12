from .. import db
import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    apellido = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True, index=True)
    role = db.Column(db.String(45), nullable=False, default="cliente")
    telefono = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=dt.datetime.now(), nullable=False)
    compras = db.relationship('Compra', back_populates="usuario", cascade="all, delete-orphan")
    
    """Please note that on the 'email' attribute, we declared it as 'unique=True' meaning that an email address can exist
       only once in our DataBase"""
       
    
    @property
    def plain_password(self):
        raise AttributeError('password can\'t be read')
    
    @plain_password.setter
    def plain_password(self, password):
        """This function will change the plain password of the user to a encrypted one using a Hash, please note that 
           it does not matters the length of the password, the Hashs will be always the same length, like for example 
           the identifiers or Hashs from Git"""
        self.password = generate_password_hash(password)
           
           
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    
    # This function we will most likely not use it. Its main purpose is for debugging in case something is wrong
    def __repr__(self):
        return f'{self.nombre}'
    
    
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'role': self.role,
            'fecha': str(self.fecha_registro)
        }
        return usuario_json
    
    
    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        apellido = usuario_json.get('apellido')
        email = usuario_json.get('email')
        telefono = usuario_json.get('telefono')
        password = usuario_json.get('password')
        role = usuario_json.get('role')
        fecha_registro = usuario_json.get('fecha_registro')
        return Usuario(
            id = id,
            nombre = nombre,
            apellido = apellido,
            email = email,
            telefono = telefono,
            plain_password = password,
            role = role,
            fecha_registro = fecha_registro 
        )
        