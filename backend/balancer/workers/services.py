from asyncio import TimeoutError, wait_for
from math import sqrt
from django.core.handlers.base import asyncio
from fastapi import  WebSocket, WebSocketDisconnect
from django.conf import settings

Workers = settings.REDIS_CLIENT


async def is_connected(websocket: WebSocket):
    try:
        await wait_for(websocket.receive_bytes(), timeout=0.0001)
    except WebSocketDisconnect:
        return False
    except TimeoutError:
        return True


def distance(point_1, point_2):
    return sqrt((point_1['x'] - point_2['x']) ** 2 + (point_1['y'] - point_2['y']) ** 2)


def change_cliets_count(port, count):
    Workers[port]["clients_count"] = int(Workers[port]["clients_count"]) + count


def add_client(port):
    change_cliets_count(port, 1)


def delete_client(port):
    change_cliets_count(port, -1)

