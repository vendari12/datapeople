import logging
from asyncio import get_event_loop, get_running_loop, run, set_event_loop
from math import ceil
from typing import Any, AsyncGenerator, Dict, List

from aiohttp import ClientSession
from pydantic import HttpUrl
from server.settings import settings
from server.utils.celery import celery
from server.utils.constants import USA_JOBS_INDEX
from server.utils.elasticsearch import ElasticsearchJobIndexer
from server.utils.usa_job_client import USAJobBoardClient


async def fetch_usa_jobs_historical_data_by_batch() -> AsyncGenerator[List[Dict[str, Any]], None]:
    """
    Fetch job announcements from the USAJobs API in batches.

    Yields:
        List[Dict[str, Any]]: A batch of job announcements.
    """
    client = USAJobBoardClient()
    page = 1
    page_size = 1000

    # Fetch the first page to determine total pages
    response = await client.fetch_paginated_historical_job_announcements(page, page_size)
    total_count = response["paging"]["metadata"]["totalCount"]
    total_pages = ceil(total_count / page_size)

    # Yield the first batch
    yield response["data"]

    # Fetch remaining pages and yield each batch
    for page in range(2, total_pages + 1):
        response = await client.fetch_paginated_historical_job_announcements(page, page_size)
        yield response["data"]

async def process_and_store_historical_jobs():
    """
    Process and store job announcements using the data fetched in batches.
    """
    elastic_client = ElasticsearchJobIndexer(USA_JOBS_INDEX)
    # create index if it doesn't exist
    await elastic_client.create_index_if_not_exists()
    async for job_batch in fetch_usa_jobs_historical_data_by_batch():
        # Process the batching and indexingg elasticsearch
        logging.info(f"Processing batch of {len(job_batch)} jobs.")
        await elastic_client.bulk_index_jobs(job_batch)
    # close elastic connection
    await elastic_client.close()
    

@celery.task
def load_daily_jobs():
    pass
        