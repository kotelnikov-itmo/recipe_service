from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from recipes.api.routes import router as api_router
from auth.api.routes import router as auth_router
from auth.api.utils import get_current_user

from conf import get_settings

settings = get_settings()


def _abs_url(rel_path: str) -> str:
    return "/".join([settings.api_root_url, rel_path])


app = FastAPI(
    title="Recipe Service",
    version="2.0",
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
app.include_router(
    auth_router,
    prefix=settings.api_root_url + "/auth",
    tags=['Auth']
)
app.include_router(
    api_router,
    prefix=settings.api_root_url,
    tags=['Recipes'],
    dependencies=[Depends(get_current_user),]
)
