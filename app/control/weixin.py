from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel


from loguru import logger

from hashlib import sha1
# 实际的子路由
router = APIRouter()

# model
class WechatRequest(BaseModel):
    signature: str
    timestamp: str
    nonce: str
    echostr: str

def checkSignature(signature, timestamp, nonce):
    token = '32f93c09ffef7e3b8ca3c276ddb1ad6c'
    arr = [token, timestamp, nonce]
    arr.sort()
    hexsha1 = sha1()
    map(hexsha1.update, arr)
    hashcode = hexsha1.hexdigest()
    logger.debug(f'hashcode:{hashcode}')
    # newarr = ''.join(arr)
    # res = sha1().hexdigest(newarr)
    return True if hashcode==signature else False


@router.get('/weixinCheckToken')
async def weixin_check_token(signature: str, timestamp: str,nonce: str,echostr: str):
    logger.debug(f'signature:{signature}')
    res = checkSignature(signature, timestamp, nonce)
    logger.debug(f'checkresult:{res}')
    return echostr if res else False


