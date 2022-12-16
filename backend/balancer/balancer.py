import socket
from contextlib import closing
from time import sleep
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import workers
from uvicorn import Config, Server
from multiprocessing import Process
from django.conf import settings
from balancer.models import WorkersSettings
from asgiref.sync import sync_to_async
from fastapi import HTTPException
import os
import signal


middleware = {
    "middleware_class": CORSMiddleware,
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}
Workers = settings.REDIS_CLIENT


async def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]


async def create_worker():
    workers_settings = await sync_to_async(WorkersSettings.objects.first)()
    if len(Workers.keys) + 1 > workers_settings.max_servers_count:
        return -1

    port = await get_free_port()

    sub_app = FastAPI()
    sub_app.add_middleware(**middleware)
    workers.attach_routers(sub_app)
    config = Config(app=sub_app, port=port)

    func = lambda config: Server(config=config).run()
    process = Process(target=func, args=[config])
    process.start()
    Workers[port] = {"clients_count": 0, "pid": process.ident, "max_clients_count": workers_settings.clients_count}

    return port

def get_load(port):
    return float(Workers[port]["clients_count"]) / float(Workers[port]["max_clients_count"]) * 100


async def get_min_loaded_worker():
    min_load = 100
    res_port = -1
    for port in Workers.keys:
        load = get_load(port)
        if min_load < load:
            min_load = load
            res_port = port

    return res_port

def check_to_remove():
    while True:
        workers_settings = WorkersSettings.objects.first()
        sleep(workers_settings.worker_timeout * 60)
        server_count = len(Workers.keys)
        for port in Workers.keys:
            if int(Workers[port]["clients_count"]) == 0 and workers_settings.min_servers_count < server_count:
                server_count -= 1
                os.kill(int(Workers[port]["pid"]), signal.SIGTERM)
                Workers.delete(port)


async def create_worker_batch(number):
    for _ in range(number):
        await create_worker()

async def get_worker():

    workers_settings = await sync_to_async(WorkersSettings.objects.first)()
    result_port = -1
    for port in Workers.keys:
        if get_load(port) < workers_settings.prefered_load:
            result_port = port

    if result_port == -1:
        result_port = await get_min_loaded_worker()
    if result_port == -1:
        result_port = await create_worker()
    if result_port == -1:
        raise HTTPException(status_code=400, detail="There is no more servers, please wait")

    return {"port": result_port}

