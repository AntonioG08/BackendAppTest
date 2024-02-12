from .. import jwt 
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    def decoration(function):
        def wrapper(*args, **kwargs):
            # Check if the JWT is the right one
            verify_jwt_in_request()
            # We retrieve the claims (requests), that are inside the JWT
            claims = get_jwt()
            
            if claims['sub']['role'] in roles:
                return function(*args, **kwargs)
            else:
                return 'Error, Role not allowed', 403
        return wrapper
    return decoration


# These are decorators that the JWT already has, however, here we are doing modifications to them
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return {
        'usuarioId': usuario.id,
        'role': usuario.role
    }
    
@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'id': usuario.id,
        'role': usuario.role,
        'emial': usuario.email
    }