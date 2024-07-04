import asyncio
from contextlib import asynccontextmanager
from base import BaseFastAPI
from typer import Typer
from celery.apps.beat import Beat
from server.utils.celery import celery
from server.utils.elasticsearch import elastic_client
from server.settings import settings
from server.routes.router import router
from server.tasks.pull_usa_jobs_to_elastic import process_and_store_historical_jobs


cli = Typer()


@asynccontextmanager
async def setup_elastic(app: BaseFastAPI):
    try:
        yield
    finally:
        await elastic_client.close()


async def load_historical_jobs_dataset():
    await process_and_store_historical_jobs()


app = BaseFastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_VI_STR}/openapi.json",
    docs_url=f"{settings.API_VI_STR}",
    redoc_url=f"{settings.API_VI_STR}/redocs",
    lifespan=setup_elastic,
)
app.include_router(router, prefix=settings.API_VI_STR)


@cli.command()
def run_load_historical_jobs():
    asyncio.run(load_historical_jobs_dataset())
    

@cli.command()
def run_celery_beat_worker():
    """Triggers a celery beat worker process"""
    b = Beat(app=celery, loglevel="debug")
    b.run()


@cli.command()
def run_cron_worker():
    """Triggers a celery worker process"""
    worker = celery.Worker()
    worker.start()


if __name__ == "__main__":
    cli()
