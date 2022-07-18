# 一个原神模拟抽卡API
## 简介
使用FastAPI编写的一个简单的原神模拟抽卡api

## 特点
- 直接返回十连抽卡图片
- 支持获取详细抽卡数据
- 支持武器定轨

没有使用数据库，直接采用`json`文件存储<br>
与官方卡池同步，暂不支持自定义卡池

## 使用方法
- 1、克隆本仓库`git clone https://github.com/CMHopeSunshine/GenshinGachaAPI`
- 2、进入目录，安装依赖`pip install -r requirements.txt`
- 3、启动Web服务器`uvicorn main:app --reload --port 9999`
9999为端口号，自行更换

## 接口说明
### 模拟抽卡接口
| 请求类型 | 接口地址                     | 说明     |
|------|--------------------------|--------|
| GET  | /genshin/gacha/role1     | 角色1池十连 |
| GET  | /genshin/gacha/role2     | 角色2池十连 |
| GET  | /genshin/gacha/weapon    | 武器池十连  |
| GET  | /genshin/gacha/permanent | 常驻池十连  |

#### 参数

| 类型  | 参数      | 说明   |
|-----|---------|------|
| int | user_id | 用户id |

#### 响应
抽卡图片

#### 示例
`http://127.0.0.1:9999/genshin/gacha/role1?user_id=1234`

### 定轨接口
| 请求类型 | 接口地址              | 说明   |
|------|-------------------|------|
| POST | /genshin/gacha/dg | 定轨武器 |

#### 请求体参数

| 类型  | 参数          | 说明       |
|-----|-------------|----------|
| int | user_id     | 用户id     |
| str | weapon_name | 所定轨武器的全称 |

#### 响应
| code | 说明       |
|------|----------|
| 0    | 定轨成功     |
| 200  | 已经定轨过该武器 |
| 500  | 该武器不在up中 |

#### 示例
- POST
`http://127.0.0.1:9999/genshin/gacha/dg`
- 请求体
```json
{
  "user_id": 1234,
  "weapon_name": "四风原典"
}
```

### 模拟抽卡详细数据接口
| 请求类型 | 接口地址                | 说明       |
|------|---------------------|----------|
| GET  | /genshin/gacha_data | 获取详细抽卡数据 |

#### 参数

| 类型  | 参数      | 说明   |
|-----|---------|------|
| int | user_id | 用户id |

#### 响应
| code | 说明       |
|------|----------|
| 0    | 获取抽卡数据成功 |
| 200  | 尚未有抽卡数据  |

#### 示例
`http://127.0.0.1:9999/genshin/gacha_data?user_id=1234`

## 感谢
- [egenshin](https://github.com/pcrbot/erinilis-modules/tree/master/egenshin) - 原始抽卡代码和资源来源