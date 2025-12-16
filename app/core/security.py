import jwt
import datetime

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer('login')

SECRET_KEY = '250nf79345jk'
ALGORITHM = 'HS256'
TOKEN_EXPIRE = 30

def create_access_token(data: dict):
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRE)
    data['exp'] = expire_time

    return jwt.encode(data, SECRET_KEY, ALGORITHM)

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        pass
    except jwt.InvalidTokenError:
        pass
