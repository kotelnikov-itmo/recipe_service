from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import router as api_router
from conf import get_settings

settings = get_settings()


def _abs_url(rel_path: str) -> str:
    return "/".join([settings.api_root_url, rel_path])


app = FastAPI(
    title="Recipe Service",
    version="1.0",
    debug=settings.debug,
    docs_url=_abs_url("docs"),
    redoc_url=_abs_url("redoc"),
    openapi_url=_abs_url("openapi.json")
)

# register middleware
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)

# register route
app.include_router(api_router, prefix=settings.api_root_url)
