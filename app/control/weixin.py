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
    token = '32f93c09ffef7e3b8ca3c276ddb1ad6c3dd23ae0bed4f364f12ac5fd98341f71'
    arr = [token, timestamp, nonce]
    arr.sort()
    newarr = ''.join(arr)
    res = sha1().hexdigest(newarr)
    return True if res==signature else False


@router.get('/weixinCheckToken')
async def weixin_check_token(wxreq: WechatRequest):
    res = checkSignature(wxreq.signature, wxreq.timestamp, wxreq.nonce)
    return wxreq.echostr if res else False


