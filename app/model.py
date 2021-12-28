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
