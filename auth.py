import jwt
import datetime
import bcrypt
import sqlite3
import secrets

#Generate token
def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
        'iat': datetime.datetdime.utcnow(),
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
    #Check if account exists
    new_user_id = ''
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM user WHERE username=?', (username))
    connection.commit()

    if len(cursor.fetchall()) != 0:
        return 'Account Conflict'
    
    #Generate unique id
    not_generated = True
    while not_generated:
        new_user_id = secrets.token_urlsafe(128)
        cursor.execute('SELECT * FROM user WHERE user_id=?',(new_user_id))
        connection.commit()

        if len(cursor.fetchall()) == 0:
            not_generated = False
    
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    cursor.execute('INSERT INTO user (user_id, username, password) VALUES (?, ?, ?)', (new_user_id, username, hashed))
    connection.commit()
    
    connection.close()
    
    return new_user_id

def verify_password(username, password):
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT user_id, password FROM user WHERE username=?', (username))
    connection.commit()
    
    output = cursor.fetchall()
    
    if len(output) == 0:
        connection.close()
        return 'Not Found'
    
    if bcrypt.checkpw(password, output[0][1]):
        connection.close()
        return output[0][0]
    else:
        connection.close()
        return 'Invalid Password'

def delete_account(username, password):
    connection = sqlite3.connect('SmallTasks_Data.db')
    cursor = connection.cursor()

    id = verify_password(username, password)

    if id == 'Not Found' or id == 'Invalid Password':
        connection.close()
        return id
    
    
    
        
        
    
    
    

    

    
