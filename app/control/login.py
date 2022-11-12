from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union

from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from random import random, choice

from loguru import logger

from models.user import add_login_user, get_user_info

# 实际的子路由
router = APIRouter()

# model
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None]=None

class UserLogin(BaseModel):
    username: str
    password: str

class BaseUser(BaseModel):
    username: str
    email: Union[str, None] =None
    disable: Union[bool, None]=None

class CreateUser(BaseUser):
    password: str

class UserInDb(BaseUser):
    hashed_password: str

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/login/token')

""" 校验密码 """
def verify_password(plain_password, hashed_password):
    
    return pwd_context.verify(plain_password, hashed_password)

""" 哈希密码 """
def get_password_hashed(password):
    return pwd_context.hash(password)

""" sql中获取user信息 """
async def get_user(username: str):
    user = await get_user_info(username)
    logger.debug(f'user:{user}')
    if user:
        user_dict = {
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "disable": user.disable,
        }
        return UserInDb(**user_dict)

""" 验证用户合法性 """
async def authenticate_user(username:str,password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict,expires_delta:Union[timedelta, None]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends()):
    users_db = await get_user(form_data.username)
    if users_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='username is not exist'
        )
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate':'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub':user.username}, expires_delta=access_token_expires
    )
    return {'access_token':access_token, 'token_type':'Bearer'}

""" root权限验证 """
async def get_root_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if not user.username=='bingo':
        raise credentials_exception
    return user

async def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get('sub')
        if username is None:
            logger.debug(1111111111)
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        logger.debug(222222222)
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        logger.debug(333333333)
        raise credentials_exception
    return user

async def get_current_active_user(current_user: BaseUser=Depends(get_current_user)):
    if current_user.disable:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Inactive user'
        )
    return current_user

@router.get('/users/me', response_model=BaseUser)
async def read_user_me(current_user: BaseUser=Depends(get_current_active_user)):
    return current_user

@router.get('/users/info', dependencies=[Depends(verify_token)])
async def read_user_me():
    data = {
        'roles':['admin'],
        # 'avatar':'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'avatar':'https://ts1.cn.mm.bing.net/th/id/R-C.a28cf610c2e9ab0933746fc1e05fd0bf?rik=cog%2fbctyyiUbvg&riu=http%3a%2f%2f5b0988e595225.cdn.sohucs.com%2fimages%2f20190531%2f29f159830727425db827cdd55e1e276a.gif&ehk=qkPTGbcBmPN7%2bpFP5zz2fYMF%2fKlEx4Sqh7kk6%2bPyK2c%3d&risl=&pid=ImgRaw&r=0',
        'userType':'Supper admin'
        }
    return {'code':20000,'data':data}

@router.get('/transaction/list')
async def transaction_list():
    data = {
        'total':20,
        'items': [{'order_no':'abc123','timestamp':'20221022','username':'john','price':1500,'status':choice(['success', 'pending'])} for n in range(20)],
        # 'items|20':[{
        #     'order_no': '@guid()',
        #     'timestamp': "+Mock.Random.date('T')",
        #     'username': '@name()',
        #     'price': '@float(1000, 15000, 0, 2)',
        #     'status|1': ['success', 'pending']
        #   }]
        }
    return {'code':20000,'data':data}

@router.post('/users/logout')
async def read_user_me():
    return {'code':20000,'data':'success'}

@router.get('/test')
async def test_api():
    return True

@router.post('/users/login')
async def user_login(userinfo: UserLogin):
    users_db = await get_user(userinfo.username)
    if users_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='username is not exist'
        )
    user = await authenticate_user(userinfo.username, userinfo.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate':'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub':user.username}, expires_delta=access_token_expires
    )
    return {'code':20000,'access_token':access_token, 'token_type':'Bearer'}

@router.post('/create/user', response_model=BaseUser, dependencies=[Depends(get_root_user)])
async def create_users(user: CreateUser):
    password = user.password
    hashed_password = pwd_context.hash(password)
    logger.debug(hashed_password)
    user.password = hashed_password
    new_user = await add_login_user(user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='user is already exist'
        )
    return user
    