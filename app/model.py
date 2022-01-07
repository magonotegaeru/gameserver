import json
import uuid
from enum import Enum, IntEnum
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import expression

from .db import engine


class InvalidToken(Exception):
    """指定されたtokenが不正だったときに投げる"""


class SafeUser(BaseModel):
    """token を含まないUser"""

    id: int
    name: str
    leader_card_id: int

    class Config:
        orm_mode = True

# 仕様：https://github.com/KLabServerCamp/gameserver/blob/main/docs/api.md#livedifficulty
# 参考サイト：
    # https://qiita.com/macinjoke/items/13aa9ba64cf9b688e74a


class LiveDifficulty(Enum):
    normal = 1
    hard = 2

class JoinRoomResult(Enum):
    Ok = 1
    RoomFull = 2
    Disbanded = 3
    OtherError = 4


class WaitRoomStatus(Enum):
    Waiting = 1
    LiveStart = 2
    Dissolution = 3


# Enum型とBasemodel型の違いってなんだ？
class RoomInfo(BaseModel):
    room_id: int
    live_id: int
    joined_user_count: int
    max_user_count: int


class RoomUser(BaseModel):
    user_id: int
    name: str
    leader_card_id: int
    select_difficulty: LiveDifficulty
    is_me: bool
    is_host: bool


class ResultUser(BaseModel):
    user_id: int
    judge_count_list: list[int]
    score: int


def create_user(name: str, leader_card_id: int) -> str:
    """Create new user and returns their token"""
    token = str(uuid.uuid4())
    # uuidは、何かのidを設定するときによく使用される乱数生成器みたいなもの。
    # NOTE: tokenが衝突したらリトライする必要がある.
    with engine.begin() as conn:
        result = conn.execute(
            text(
                "INSERT INTO `user` (name, token, leader_card_id) VALUES (:name, :token, :leader_card_id)"
            ),
            {"name": name, "token": token, "leader_card_id": leader_card_id},
        )
        # print(result)
    return token


def _get_user_by_token(conn, token: str) -> Optional[SafeUser]:
    # TODO: 実装
    # res = conn.execute(text("select * from user where token='wdUZxFXT'"))
    result = conn.execute(
        text("SELECT `id`, `name`, `leader_card_id` FROM `user` WHERE `token`=:token"),
        dict(token=token),
    )
    try:
        row = result.one()
    except NoResultFound:
        return None
    return SafeUser.from_orm(row)
    # Configでorm_mode=TrueしておくとSafeUser.from_orm(row)が使える。
    # このメソッドは次と同じ。
    # SafeUser(id=row.id, name=row.name,leader_card_id=row.leader_card_id)


def get_user_by_token(token: str) -> Optional[SafeUser]:
    with engine.begin() as conn:
        return _get_user_by_token(conn, token)


# 久しぶりだからメモ
# from app.model import get_user_by_token
# で他で使用できるようになる。


def update_user(token: str, name: str, leader_card_id: int) -> None:
    # このコードを実装してもらう
    with engine.begin() as conn:
        # TODO: 実装
        user = _get_user_by_token(conn, token)
        conn.execute(
            text(
                "UPDATE `user` SET `name`=:name,`leader_card_id`=:leader_card_id WHERE `id`=:id"
            ),
            # dict(name=name, leader_card_id=leader_card_id, id=user.id)
            {"name": name, "leader_card_id": leader_card_id, "id": user.id}
            # text(f"UPDATE `user` SET `name`={name} `leader_card_id`=:{leader_card_id} WHERE `id`={user.id}"),
        )
        pass

# def create_room() -> None:
#     with engine.begin() as conn:
#         # user = _get_user_by_token(conn, token)
#         # conn.execute("DROP TABLE IF EXISTS `room`")
#         conn.execute(
#             # https://github.com/KLabServerCamp/gameserver/blob/main/docs/api.md
#             # 参照
#             text("CREATE TABLE `room` (`room_id` int,`live_id` int,`joined_user_count` int,`max_user_count` int)")
#         )
#         conn.execute(
#             text("INSERT INTO `room` SET `room_id` = :room_id,`live_id` = :live_id,`joined_user_count` = :joined_user_count,`max_user_count` = :max_user_count"),
#             {"room_id":1,"live_id":11,"joined_user_count":111,"max_user_count":1111}
#         )
#         pass
# 1228
# とりあえず、テーブルをサーバ側に送ることはできた。

def create_room(room_id: int,live_id: int) -> None:
    # Room = RoomInfo(room_id=int(uuid.uuid4()), joined_user_count=1, max_user_count=4)
    Room = RoomInfo(room_id=room_id, live_id=live_id, joined_user_count=1, max_user_count=4)
    with engine.begin() as conn:
        # conn.execute(
        #     text("CREATE TABLE `room` (`room_id` int,`live_id` int,`joined_user_count` int,`max_user_count` int)")
        # )
        conn.execute(
            text("INSERT INTO `room` SET `room_id` = :room_id,`live_id` = :live_id,`joined_user_count` = :joined_user_count,`max_user_count` = :max_user_count"),
            {"room_id":Room.room_id,"live_id":Room.live_id,"joined_user_count":Room.joined_user_count,"max_user_count":Room.max_user_count}
        )
        # return Room.room_id
        pass

def insert_room_member(room_id: int, user_id: int) -> None:
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO `room_member` SET `room_id` = :room_id,`user_id` = :user_id"),
            {"room_id":room_id,"user_id":user_id}
        )
        pass

# def get_room_list(live_id: int) -> list[RoomInfo]:
def get_room_list(live_id: int):
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT * FROM `room` WHERE `live_id` = :live_id"),
            {"live_id":live_id}
        )
        try:
            row = result.all()
        except NoResultFound:
            return None
        # print(row)
        return row

def join_room(room_id: int, user_id: int) -> JoinRoomResult:
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT `joined_user_count`, `max_user_count` FROM `room` WHERE `room_id` = :room_id"),
            {"room_id":room_id}
        )
        try:
            row = result.all()
        except NoResultFound:
            return JoinRoomResult.Disbanded
        
    joined_user_count = int(row[0]["joined_user_count"])
    max_user_count = int(row[0]["max_user_count"])

    if (joined_user_count < max_user_count):
        new_joined_user_count = joined_user_count + 1
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE `room` SET `joined_user_count`=:new_joined_user_count WHERE `room_id`=:room_id"),
                {"new_joined_user_count":new_joined_user_count, "room_id":room_id}
            )
            conn.execute(
                text("INSERT INTO `room_member` SET `room_id` = :room_id,`user_id` = :user_id"),
                {"room_id":room_id,"user_id":user_id}
            )
            return JoinRoomResult.Ok
    
    elif (joined_user_count == max_user_count):
        return JoinRoomResult.RoomFull
    
    else :
        return JoinRoomResult.OtherError

# 0107 タスク３（join/room）まで、何とか実装できた。




