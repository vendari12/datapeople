import logging
from datetime import datetime, timezone
from http import HTTPMethod, HTTPStatus
from typing import Any, Dict, Optional, Union

import backoff
from aiohttp import (ClientConnectionError, ClientError, ClientResponse,
                     ClientSession, ContentTypeError)
from server.settings import settings  
from server.utils.exceptions import (  
    USAJobClientManagementError, USAManagementJsonError)

# Base URL for the USA Jobs API
_USA_JOBS_BASE_URL = "https://data.usajobs.gov/api/"

# Initialize the logger
logger = logging.getLogger(__name__)

from datetime import datetime, timezone


def parse_datetime(datetime_str):
    try:
        # Try parsing as ISO 8601 without timezone (e.g., "2016-12-05T00:00:00")
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        pass

    try:
        # Try parsing as ISO 8601 with timezone
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError as e:
        raise ValueError(f"Unsupported datetime format: {datetime_str}") from e


def normalize_datetime(datetime_obj: datetime):
    # Normalize datetime to UTC timezone if it has timezone info
    if datetime_obj.tzinfo is not None:
        return datetime_obj.astimezone(timezone.utc)
    else:
        # Assume naive datetime is in UTC
        return datetime_obj.replace(tzinfo=timezone.utc)


async def parse_response(response: ClientResponse) -> Union[Dict, str]:
    """
    Parse the response content to JSON or text.

    Arguments:
        response: ClientResponse object from aiohttp request.

    Returns:
        Union[Dict, str]: Parsed response content.
    """
    try:
        return await response.json()
    except ContentTypeError:
        return await response.text()


class USAJobBoardClient:
    """
    Client for interacting with the USAJobBoard service.
    """

    def __init__(self) -> None:
        self._base_url = _USA_JOBS_BASE_URL
        self.host = "data.usajobs.gov"

    @property
    def _default_headers(self) -> Dict[str, str]:
        """
        Retrieve the default request headers including the JWT.

        Returns:
            Dict[str, str]: Default request headers.
        """
        return {
            "Host": self.host,
            "User-Agent": settings.ADMIN_EMAIL,
            "Authorization-Key": settings.JOB_API_KEY,
        }

    def _build_url(self, path: str) -> str:
        """
        Construct the full URL for the given API path.

        Arguments:
            path: The endpoint path to resource.

        Returns:
            str: Fully qualified URL.
        """
        return f"{self._base_url}{path}"

    @backoff.on_exception(
        backoff.expo, (ClientError, ClientConnectionError), max_time=60, max_tries=3
    )
    async def _get(
        self, path: str, headers: Optional[Dict[str, str]] = None, **kwargs
    ) -> Any:
        """
        Make an HTTP request with the given method, path, and parameters.

        Arguments:
            path: API endpoint path.
            headers: Optional additional headers.
            **kwargs: Additional parameters for aiohttp request.

        Returns:
            Any: Parsed response content.

        Raises:
            USAJobClientManagementError: If the request fails.
        """
        url = self._build_url(path)
        request_headers = {**self._default_headers, **(headers or {})}

        async with ClientSession() as session:
            async with session.request(
                HTTPMethod.GET, url, headers=request_headers, **kwargs
            ) as response:
                if response.status == HTTPStatus.OK:
                    return await parse_response(response)

                error_details = await parse_response(response)
                logger.warning(
                    f"Request failed for {HTTPMethod.GET} {url}. "
                    f"Status code: {response.status}, Error details: {error_details}"
                )
                raise USAJobClientManagementError(
                    response.status,
                    f"Request to {url} failed with status code {response.status}. Details: {error_details}",
                )

    async def search_jobs_by_fields(
        self, fields: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Search for jobs using specified fields.

        Arguments:
            fields: Dictionary of search fields.

        Returns:
            Optional[Dict[str, Any]]: Search results if available.

        Raises:
            USAJobClientManagementError: If the request fails.
        """
        return await self._get("search", params=fields)

    async def fetch_paginated_historical_job_announcements(
        self, page: int, page_size: int = 1000, params: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch paginated historical job announcements.

        Arguments:
            page: Page number to fetch.
            page_size: Number of results per page.
            params: Optional dictionary of additional parameters.

        Returns:
            Optional[Dict[str, Any]]: Historical job announcements data if available.

        Raises:
            USAJobClientManagementError: If the request fails.
        """
        params = params or {}
        params.update({"Pagesize": page_size, "PageNumber": page})

        return await self._get("historicjoa", params=params)


def _parse_job_data_with_date(job: Dict):
    for field, value in job.items():
        pass
