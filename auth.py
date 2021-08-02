import jwt
import datetime
import cryptography

#Generate token
def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }

    return jwt.encode(payload, 'secret', algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, 'secret')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Expired'
    except jwt.InvalidTokenError:
        return 'Invalid'

def create_account(username, password):
    