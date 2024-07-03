from elasticsearch import AsyncElasticsearch, helpers, NotFoundError
import logging

logger = logging.getLogger(__name__)

elastic_client = AsyncElasticsearch()


class ElasticsearchJobIndexer:
    """
    Class to handle indexing jobs into Elasticsearch.
    """
    
    def __init__(self, index: str):
        self.es = elastic_client
        self.index = index

    async def create_index_if_not_exists(self) -> None:
        """
        Create the Elasticsearch index if it doesn't exist.
        """
        try:
            await self.es.indices.get(index=self.index)
            logger.info(f"Index '{self.index}' already exists.")
        except NotFoundError:
            await self.es.indices.create(index=self.index)
            logger.info(f"Index '{self.index}' created successfully.")

    async def bulk_index_jobs(self, jobs: list[dict]) -> None:
        """
        Bulk index the job announcements into Elasticsearch.

        Arguments:
            jobs: List of job announcement dictionaries to index.
        """
        actions = [
            {
                "_index": self.index,
                "_id": job.get("JobID", ""),
                "_source": job
            }
            for job in jobs
        ]

        try:
            response = await helpers.async_bulk(self.es, actions)
            logger.info(f"Bulk indexed {len(jobs)} jobs successfully: {response}")
        except Exception as e:
            logger.error(f"Failed to bulk index jobs: {str(e)}")

    async def close(self):
        """
        Close the Elasticsearch connection.
        """
        await self.es.close()