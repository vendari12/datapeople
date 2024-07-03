import logging
import os
from typing import Optional
from redis.asyncio import Redis as AIORedis
from server.settings import settings

_REDIS_CERT_PATH = os.environ.get("REDIS_CERT_PATH")


def read_redis_password() -> Optional[str]:
    """
    Reads the Redis password from a file specified by the `_REDIS_CERT_PATH` environment variable.

    Returns:
        Optional[str]: The Redis password if the file exists, None otherwise.
    """
    if _REDIS_CERT_PATH:
        try:
            with open(_REDIS_CERT_PATH, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            logging.error(f"Couldn't load Redis password from path: {_REDIS_CERT_PATH}")
            return None
    return None


# Cache the Redis password to avoid reading the file multiple times
_REDIS_PASSWORD = read_redis_password()


def build_redis_connection_args() -> dict:
    """
    Builds the connection arguments for connecting to the Redis server.

    This function considers SSL configuration and other settings from the environment.

    Returns:
        dict: A dictionary containing the connection parameters for Redis.
    """
    connection_args = {
        "host": settings.CACHE_HOST,
        "port": settings.CACHE_PORT,
        "password": _REDIS_PASSWORD,
        "db": settings.CACHE_DB
    }
    if settings.CACHE_SSL:
        connection_args.update({
            "ssl": True,
            "ssl_cert_reqs": "required",
            "ssl_ca_certs": _REDIS_CERT_PATH,
        })
    return connection_args


def get_redis_url(connection_args: dict) -> str:
    """
    Constructs the Redis URL from the given connection arguments.

    Args:
        connection_args (dict): The connection parameters for Redis.

    Returns:
        str: The constructed Redis URL.
    """
    scheme = "rediss" if connection_args.get("ssl") else "redis"
    password = f":{connection_args['password']}@" if connection_args.get("password") else ""
    host_port = f"{connection_args['host']}:{connection_args['port']}"
    db = f"/{connection_args['db']}"
    ssl_options = f"?ssl_cert_reqs=required&ssl_ca_certs={connection_args['ssl_ca_certs']}" if connection_args.get("ssl") else ""

    return f"{scheme}://{password}{host_port}{db}{ssl_options}"


def get_redis_client(**kwargs) -> AIORedis:
    """
    Creates an asynchronous Redis client using either provided arguments or default settings.

    Args:
        **kwargs: Arbitrary keyword arguments to override the default connection parameters.

    Returns:
        AIORedis: The initialized asynchronous Redis client.
    """
    if kwargs:
        return AIORedis(**kwargs)
    else:
        return AIORedis(**build_redis_connection_args())
