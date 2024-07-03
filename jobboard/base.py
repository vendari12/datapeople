from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware


class BaseFastAPI(FastAPI):
    """ 
        Extends the FastAPI base class
        with some extra batteries, like CORS support
        GZIP Compression
        
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                            allow_methods=["*"], allow_headers=["*"])
        self.add_middleware(GZipMiddleware, minimum_size=1000)