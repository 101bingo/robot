from fastapi import APIRouter

# 导入实际的控制文件
from control import fish_run,login

api_router = APIRouter()

# 添加实际控制的路由
api_router.include_router(fish_run.router, prefix="/fish")
api_router.include_router(login.router, prefix="/login")