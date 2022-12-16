from fastapi import BackgroundTasks, FastAPI
import uvicorn
from threading import Thread
import os
from asgiref.sync import sync_to_async
from django.conf import settings
main_app = FastAPI()


# RUN DJANGO ALONGSIDE FASTAPI
from django.core.wsgi import get_wsgi_application
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from importlib.util import find_spec

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traveling_salesman.settings')
django_app = get_wsgi_application()


from balancer.models import WorkersSettings
from balancer.balancer import middleware, get_worker, check_to_remove, create_worker_batch
main_app.add_middleware(**middleware)


@main_app.get("/api/worker/")
async def balancer():
    return await get_worker()


main_app.mount('/static',
    StaticFiles(
         directory=os.path.normpath(os.path.join(find_spec('django.contrib.admin').origin, '..', 'static'))
   ), name='static'
)
main_app.mount("/", WSGIMiddleware(django_app))


Thread(target=check_to_remove, daemon=True).start()


@main_app.on_event("startup")
async def startup_event():
    workers_settings = await sync_to_async(WorkersSettings.objects.first)()
    await create_worker_batch(workers_settings.min_servers_count)

@main_app.on_event("shutdown")
def shutdown_event():
    settings.REDIS_CLIENT.clear()

if __name__ == '__main__':
    uvicorn.run("__main__:main_app", port=5000)

