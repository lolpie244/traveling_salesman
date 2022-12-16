from math import inf
import asyncio
from fastapi import WebSocket, APIRouter
from .services import is_connected, distance, add_client, delete_client

router = APIRouter()

async def get_min(from_point, used, points):
    min_len = inf
    id = -1
    for i, point in enumerate(points):
        if used[i]:
            continue

        new_len = distance(from_point, point)

        if new_len < min_len:
            id = i
            min_len = new_len
    return id, min_len


@router.websocket("/nearest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    add_client(websocket.url.port)
    length = 0

    data = await websocket.receive_json()
    points = data['points']
    delay = float(data['delay'])

    path = [points[0]]
    used = [False for _ in range(len(points))]
    used[0] = True

    await websocket.send_json({"at_start": False, "point": points[0]})
    while len(path) < len(points):
        if not await is_connected(websocket):
            delete_client(websocket.url.port)
            return
        id_l, min_l = await get_min(path[0], used, points)
        id_r, min_r = await get_min(path[-1], used, points)

        if min_l < min_r:
            path.insert(0, points[id_l])
            length += min_l
            used[id_l] = True
            await websocket.send_json({"at_start": True, "point": points[id_l]})
        else:
            path.append(points[id_r])
            length += min_r
            used[id_r] = True
            await websocket.send_json({"at_start": False, "point": points[id_r]})
        await asyncio.sleep(delay)


    if len(path) > 1:
        path.append(path[0])
        await websocket.send_json({"at_start": False, "point": path[0]})

    length = round(length)

    await websocket.send_json({"length": length})

    delete_client(websocket.url.port)
    await websocket.close(reason="success")

