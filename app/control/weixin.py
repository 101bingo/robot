from fastapi import APIRouter, Depends, HTTPException, status, Response
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
    arr.sort() # 排序
    hexsha1 = sha1()
    newarr = ''.join(arr) # 组成一个字符串进行sha1加密
    hexsha1.update(newarr.encode('utf-8'))
    hashcode = hexsha1.hexdigest()
    return True if hashcode==signature else False


@router.get('/weixinCheckToken')
async def weixin_check_token(signature: str, timestamp: str,nonce: str,echostr: str):
    res = checkSignature(signature, timestamp, nonce)
    logger.debug(f'checkresult:{res}')
    ret_str = echostr if res else ''
    return Response(ret_str, media_type='text/html;charset=utf-8')

