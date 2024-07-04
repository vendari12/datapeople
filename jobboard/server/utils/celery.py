from celery import Celery
from server.settings import settings
from server.utils.cache import build_redis_connection_args, get_redis_url

# Redis config

# Construct the Redis connection arguments and URL
redis_connection_args = build_redis_connection_args()
redis_url = get_redis_url(redis_connection_args)


celery = Celery(__name__)
celery.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    timezone="UTC",
    accept_content=["pickle", "json", "msgpack", "yaml"],
    worker_send_task_events=True,
)

