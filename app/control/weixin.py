from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union

import requests
import json
from loguru import logger

from hashlib import sha1
# 实际的子路由
router = APIRouter()

access_token = None

# model
class WechatRequest(BaseModel):
    signature: str
    timestamp: str
    nonce: str
    openid: str

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
async def weixin_check_token(signature: str, timestamp: str,nonce: str,echostr: Union[str, None]=None, openid: Union[str, None]=None):
    res = checkSignature(signature, timestamp, nonce)
    logger.debug(f'checkresult:{res}')
    ret_str = echostr if res else ''
    return Response(ret_str, media_type='text/html;charset=utf-8')

@router.post('/weixinCheckToken')
async def weixin_msg(req_msg: WechatRequest):
    ret_str = req_msg.openid if req_msg.openid else ''
    return Response(ret_str, media_type='text/html;charset=utf-8')



def get_access_token():
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': 'wx1a1c44f37d00378e',
        'secret': 'a87959976b0ca60702909c699f2e4280'
    }
    res = requests.get(url=access_token_url, params=params).json()
    if res.get('access_token'):
        access_token = res.get('access_token')
    else:
        access_token = None
    return access_token

def get_user_openid():
    global access_token
    access_token = get_access_token()
    # access_token = 'get_access_token'
    user_openid_url = 'https://api.weixin.qq.com/cgi-bin/user/get'
    params = {
        'access_token': access_token
    }
    res = requests.get(url=user_openid_url, params=params).json()
    logger.debug(f'get_user_openid:{res}')
    return res['data'].get('openid') if res.get('data') else []

def get_user_code():
    code_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1a1c44f37d00378e&redirect_uri=https%3A%2F%2Fchong.qq.com%2Fphp%2Findex.php%3Fd%3D%26c%3DwxAdapter%26m%3DmobileDeal%26showwxpaytitle%3D1%26vb2ctag%3D4_2030_5_1194_60&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
    params = {
        'appid': 'wx1a1c44f37d00378e',
        'redirect_uri':'https%3A%2F%2Fchong.qq.com%2Fphp%2Findex.php%3Fd%3D%26c%3DwxAdapter%26m%3DmobileDeal%26showwxpaytitle%3D1%26vb2ctag%3D4_2030_5_1194_60',
        'response_type':'code',
        'scope':'snsapi_base',
        'state':12
    }
    res = requests.get(url=code_url)
    print(res.text)

def send_msg(openid, msg):
    send_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
    access_token = get_access_token()
    body = {
        'touser': openid,
        'msgtype': 'text',
        'text': {
            'content': msg,
        }
    }
    response = requests.post(url=send_msg_url, params={'access_token':access_token}, data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8'))
    result = response.json()

    print(result)

def send_msg_by_temple(date_time, oxygen, temper):
    # global access_token
    # send_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend'
    send_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
    # access_token = get_access_token()
    user_list = get_user_openid()
    for user_openid in user_list:
        body = {
            'touser': user_openid,
            'template_id': 'mTxYHJBK-BqnGwvTX4jFUfUfh3F6kRmWcTTumj6BqbQ',
            "url":"http://42.193.138.254:8083/", #跳转地址
            "topcolor":"#173177",
            "data": {
                "date_time": {
                    "value": str(date_time),
                    "color": "#173177"
                },
                "oxygen": {
                    "value": f"{oxygen} mg/L",
                    "color": "#d96459"
                },
                "temper": {
                    "value": f"{temper}℃"
                }
            }
        }
        response = requests.post(url=send_msg_url, params={'access_token':access_token}, data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8'))
        result = response.json()
        logger.debug(result)