from enum import Enum

from fastapi import FastAPI
from starlette.responses import Response
from pydantic import BaseModel

from draw import draw_ten_items
from data_source import set_dg_weapon
from data_handle import load_user_data

app = FastAPI()


class PoolName(str, Enum):
    role1 = 'role1'
    role2 = 'role2'
    weapon = 'weapon'
    permanent = 'permanent'


class DgBody(BaseModel):
    user_id: int
    weapon_name: str


@app.get("/genshin/gacha/{pool}")
async def gacha(pool: PoolName, user_id: int):
    img = await draw_ten_items(user_id, pool)
    return Response(img, media_type='image/png')


@app.post("/genshin/gacha/dg")
async def dg(dg_body: DgBody):
    result = await set_dg_weapon(dg_body.user_id, dg_body.weapon_name)
    return result


@app.get("/genshin/gacha_data")
async def gacha(user_id: int):
    data = load_user_data(user_id)
    if 'code' not in data:
        data = {
            'code': 0,
            'message': '获取抽卡数据成功',
            'data': data
        }
    return data
