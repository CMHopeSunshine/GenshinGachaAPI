from pathlib import Path

from data_handle import load_json
from PIL import Image, ImageDraw, ImageFont
from data_source import get_once_data, get_gacha_data
from io import BytesIO

RES_PATH = Path() / 'res'
font_path = RES_PATH / 'hywh.ttf'


def draw_center_text(draw_target, text: str, left_width: int, right_width: int, height: int, fill: str, font):
    """
    绘制居中文字
    :param draw_target: ImageDraw对象
    :param text: 文字
    :param left_width: 左边位置横坐标
    :param right_width: 右边位置横坐标
    :param height: 位置纵坐标
    :param fill: 字体颜色
    :param font: 字体
    """
    text_length = draw_target.textlength(text, font=font)
    draw_target.text((left_width + (right_width - left_width - text_length) / 2, height), text, fill=fill,
                     font=font)


def draw_single_item(rank, item_type, name, element, count, dg_time):
    type_json = load_json(RES_PATH / 'type.json', encoding="utf-8")
    count_font = ImageFont.truetype(str(font_path), 35)
    bg = Image.open(RES_PATH / f'{rank}_background.png').resize((143, 845))
    item_img = Image.open(RES_PATH / item_type / f'{name}.png')
    rank_img = Image.open(RES_PATH / f'{rank}_star.png').resize((119, 30))

    if item_type == '角色':
        item_img = item_img.resize((item_img.size[0] + 12, item_img.size[1] + 45))
        item_img.alpha_composite(rank_img, (4, 510))

        item_type_icon = Image.open(RES_PATH / '元素' / f'{element}.png').resize((80, 80))
        item_img.alpha_composite(item_type_icon, (25, 420))
        bg.alpha_composite(item_img, (3, 125))

    else:
        bg.alpha_composite(item_img, (3, 240))
        bg.alpha_composite(rank_img, (9, 635))

        item_type_icon = type_json.get(name)
        if item_type_icon:
            item_type_icon = Image.open(RES_PATH / '类型' / f'{item_type_icon}.png').resize((100, 100))

            bg.alpha_composite(item_type_icon, (18, 530))
    if rank == 5 and count != -1:
        draw = ImageDraw.Draw(bg)
        draw_center_text(draw, str(count) + '抽', 0, 143, 750, 'white', count_font)
        if dg_time != -1:
            if dg_time == 3:
                draw_center_text(draw, '定轨结束', 0, 143, 785, 'white', count_font)
            else:
                draw_center_text(draw, '定轨' + str(dg_time) + '/2', 0, 143, 785, 'white', count_font)
    return bg


async def draw_ten_items(user_id: int, pool: str):
    gacha_data = await get_gacha_data(pool)
    type_json = load_json(RES_PATH / 'type.json', encoding="utf-8")
    gacha_list = []
    for i in range(0, 10):
        role = get_once_data(user_id, gacha_data).copy()
        gacha_list.append(role)
    gacha_list.sort(key=lambda x: x["rank"], reverse=True)
    img = Image.open(RES_PATH / 'background.png')
    i = 0
    for wish in gacha_list:
        i += 1
        rank = wish['rank']
        item_type = wish['item_type']
        name = wish['item_name']
        element = wish.get('item_attr') or type_json[name]
        count = wish['count']
        try:
            dg_time = wish['dg_time']
        except KeyError:
            dg_time = -1
        i_img = draw_single_item(rank, item_type, name, element, count, dg_time)
        img.alpha_composite(i_img, (105 + (i_img.size[0] * i), 123))

    img.thumbnail((1024, 768))
    img2 = Image.new("RGB", img.size, (255, 255, 255))
    img2.paste(img, mask=img.split()[3])
    bio = BytesIO()
    img2.save(bio, format='JPEG', quality=100)
    return bio.getvalue()
