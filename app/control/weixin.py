from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel

from typing import Union
import requests
import json
import xmltodict
from loguru import logger
import time
from datetime import datetime
from hashlib import sha1
import threading

from models.fish_model import add_setting_oxygen_limit_data,get_setting_oxygen_limit_data,get_oxygen_warning_data
# 实际的子路由
router = APIRouter()

LIMIT_OXYGEN = 5
access_token = None
is_stop_warning = False

# model
class WechatRequest(BaseModel):
    signature: str
    timestamp: str
    nonce: str
    openid: str

class SetOxygenValue(BaseModel):
    oxygenData: float
    deviceInfo: str

def checkSignature(signature, timestamp, nonce):
    token = '32f93c09ffef7e3b8ca3c276ddb1ad6c'
    arr = [token, timestamp, nonce]
    arr.sort() # 排序
    hexsha1 = sha1()
    newarr = ''.join(arr) # 组成一个字符串进行sha1加密
    hexsha1.update(newarr.encode('utf-8'))
    hashcode = hexsha1.hexdigest()
    return True if hashcode==signature else False

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

def get_global_access_token():
    global access_token
    access_token = get_access_token()

def get_user_openid():
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
    # send_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend'
    send_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send'
    # user_list = get_user_openid()
    user_list = ['oZl2w6tfUnaJVFi3Bhnbj42KIhew', 'oZl2w6mdnuZuRCgjC9cZ8CkcacR4']
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

def init_warning_flag():
    global is_stop_warning
    is_stop_warning = False

def oxygen_warning(date_time, oxygen, temper):
    global is_stop_warning
    logger.debug(f'oxygen_warning stop flag:{is_stop_warning}')
    if access_token==None:
        get_global_access_token()
    while not is_stop_warning:
        logger.debug(f'oxygen_warning stop flag:{is_stop_warning}')
        send_msg_by_temple(date_time, oxygen, temper)
        time.sleep(3)

def oxygen_threading(date_time, oxygen, temper):
    # import threading
    global th_oxygen
    t1 = threading.Thread(target=oxygen_warning, args=(date_time, oxygen, temper))
    t1.setDaemon(True)
    t1.start()
    

@router.get('/getAccessToken')
def get_access_token_api():
    """ 获取access token接口的 """
    get_global_access_token()

@router.get('/stopWarning')
def test_stop_warning():
    global is_stop_warning
    is_stop_warning = True

@router.post('/setOxygenLimit')
async def set_oxygen_limit(value: SetOxygenValue):
    global LIMIT_OXYGEN
    current_time = datetime.now()
    LIMIT_OXYGEN = value.oxygenData
    upload_data = {
        'device_info': value.deviceInfo,
        'oxygen_limit': LIMIT_OXYGEN,
        'date_time': current_time
    }
    await add_setting_oxygen_limit_data(upload_data) # 写数据库
    logger.info(f'Setting oxygen limit value: {value}')
    return {'code':0,'msg': LIMIT_OXYGEN}

@router.get('/getRecordOxygenLimit')
async def get_oxygen_limit_record():
    rst = await get_setting_oxygen_limit_data() # 读数据库
    for res in rst:
        logger.debug(res.date_time)
        logger.debug(type(res.date_time))
        res.date_time = str(res.date_time).replace('-', '/')
    logger.info(f'get oxygen limit value: {rst}')
    return {'code':0,'data': rst}

@router.get('/getRecordOxygenWarning')
async def get_oxygen_limit_record():
    rst = await get_oxygen_warning_data() # 读数据库
    for res in rst:
        logger.debug(res.date_time)
        logger.debug(type(res.date_time))
        res.date_time = str(res.date_time).replace('-', '/')
    logger.info(f'get oxygen warning: {rst}')
    return {'code':0,'data': rst}

@router.get('/getOxygenLimit')
def get_oxygen_limit():
    logger.info(f'get oxygen limit value: {LIMIT_OXYGEN}')
    return {'code':0,'limit_oxygen': LIMIT_OXYGEN}

@router.get('/weixinCheckToken')
async def weixin_check_token(signature: str, timestamp: str,nonce: str,echostr: Union[str, None]=None, openid: Union[str, None]=None):
    res = checkSignature(signature, timestamp, nonce)
    logger.debug(f'checkresult:{res}')
    ret_str = echostr if res else ''
    return Response(ret_str, media_type='text/html;charset=utf-8')

@router.post('/weixinCheckToken')
async def weixin_msg(request: Request,signature: str, timestamp: str,nonce: str, openid: Union[str, None]=None):
    global is_stop_warning
    msg = await request.body()
#     msg = '''
#     <xml>
#     <ToUserName><![CDATA[toUser]]></ToUserName>
#     <FromUserName><![CDATA[fromUser]]></FromUserName>
#     <CreateTime>12345678</CreateTime>
#     <MsgType><![CDATA[text]]></MsgType>
#     <Content><![CDATA[你好]]></Content>
#     </xml>
# '''
    if msg:
        is_stop_warning = True
        request_msg = xmltodict.parse(msg)
        xml_data = request_msg.get('xml')
        logger.debug(xml_data)
        text_content = xml_data['Content']
        user_openid = xml_data['FromUserName']
        logger.debug(f'text_content:{text_content}')
        send_msg(user_openid, '报警已关闭！')
    # logger.debug(msg)
    ret_str = 'success'
    return Response(ret_str, media_type='text/xml;charset=utf-8')