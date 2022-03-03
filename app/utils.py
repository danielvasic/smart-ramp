from flask import make_response, jsonify, request, current_app
from models.user import User
from functools import wraps
# from index import app
import jwt

def custom_response(message, status_code): 
    return make_response(jsonify(message), status_code)

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
       if not token:
            message = {
                "error" : "Pristup sustavu odbijen zbog nemogućnosti dohvaćanja token-a iz zahtjeva.",
                "code" : 401
            }
            return custom_response(message, 401)
       try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'])
           user = User.query.filter_by(eduid=data['eduid']).first()
       except:
            message = {
                "error" : "Pristup sustavu odbijen zbog verificiranja ispravnosti token-a.",
                "code" : 401
            }
            return custom_response(message, 401)
       return f(user, *args, **kwargs)
   return decorator