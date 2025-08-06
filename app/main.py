import aioredis
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # для работы с картинками
from datetime import date, time
from sqladmin import Admin
# from fastapi_versioning import VersionedFastAPI  # для версионирования
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.database import engine
from app.config import settings
from app.admin.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin

# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
#
# from redis import asyncio as aioredis

from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.importer.router import router as router_import
from app.users.router import router_auth, router_users
from app.logger import logger


# подключение приложения
app = FastAPI()

# Подключение Sentry для мониторинга ошибок. Лучше выключать на период локального тестирования
if settings.MODE != "TEST":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={"continuous_profiling_auto_start": True},
    )

# подключение основных роутеров
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)

# подключение дополнительных роутеров
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_import)

# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

# для версионирования
# app = VersionedFastAPI(app,
#     version_format='{major}',
#     prefix_format='/v{major}',
# )


# используем при тестировании этот мод
# if settings.MODE == "TEST":
#     # при тестировании через pytest, необходимо подключать Redis, чтобы кэширование работало
#     # иначе декоратор @cache из библиотеки fastapi-cache ломает выполнение кэшируемых эндпоинтов
#     redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


# для мониторинга и отображения метрик, их дальнейшего сбора Прометеусом
# instrumentator = Instrumentator(
#     should_group_status_codes=False,
#     excluded_handlers=[".*admin.*", "/metrics"]
# )
# instrumentator.instrument(app).expose(app)

# для подключения админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


# подключение картинок
app.mount("/static", StaticFiles(directory="app/static"), "static")


# для логирования
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response
