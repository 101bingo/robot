from fastapi import APIRouter

# 导入实际的控制文件
from control import fish_run

api_router = APIRouter()

# 添加实际控制的路由
api_router.include_router(fish_run.router, prefix="/fish")