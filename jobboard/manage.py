import asyncio
from contextlib import asynccontextmanager
from base import BaseFastAPI
from typer import Typer
from server.utils.elasticsearch import elastic_client
from jobboard.server.settings import settings
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
app.include_router(router, prefix=settings.API_V2_STR)


@cli.command()
def run_load_historical_jobs():
    asyncio.run(load_historical_jobs_dataset())


if __name__ == "__main__":
    cli()
