import json
from pathlib import Path
from typing import Union


def load_json(path: Union[Path, str], encoding: str = 'utf-8') -> dict:
    """
    说明：
        读取本地json文件，返回json字典。
    参数：
        :param path: 文件路径
        :param encoding: 编码，默认为utf-8
        :return: json字典
    """
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        save_json({}, path, encoding)
    return json.load(path.open('r', encoding=encoding))


def save_json(data: dict, path: Union[Path, str] = None, encoding: str = 'utf-8'):
    """
    保存json文件
    :param data: json数据
    :param path: 保存路径
    :param encoding: 编码
    """
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, path.open('w', encoding=encoding), ensure_ascii=False, indent=4)


data_path = Path() / 'data'
data_path.mkdir(exist_ok=True, parents=True)


def load_user_data(user_id: int) -> dict:
    user_data_path = data_path / f'{user_id}.json'
    if not user_data_path.exists():
        new_data = {
            '抽卡数据':  {
                '抽卡总数':        0,
                '4星出货数':            0,
                '5星出货数':            0,
                '4星up出货数':         0,
                '5星up出货数':         0,
                '角色池未出5星数':      0,
                '武器池未出5星数':    0,
                '常驻池未出5星数': 0,
                '角色池未出4星数':      0,
                '武器池未出4星数':    0,
                '常驻池未出4星数': 0,
                '角色池5星下次是否为up':      False,
                '武器池5星下次是否为up':    False,
                '角色池4星下次是否为up':      False,
                '武器池4星下次是否为up':    False,
                '定轨武器名称':           '',
                '定轨能量':           0
            },
            '角色列表':   {},
            '武器列表': {}
        }
        save_json(new_data, user_data_path)
        return {'code': 200, 'message': '尚未有抽卡数据'}
    else:
        return load_json(user_data_path)


def save_user_data(user_id: int, data: dict):
    user_data_path = data_path / f'{user_id}.json'
    save_json(data, user_data_path)
