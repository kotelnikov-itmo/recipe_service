#!/usr/bin/env python3
import logging
import uvicorn
# import inspect

from app import app
from conf import get_settings

log = logging.getLogger('uvicorn')
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    settings = get_settings()
    # _uvicorn_conf_names = set(inspect.getfullargspec(uvicorn.Config.__init__)[0][2:])
    log.debug('App run with settings:')
    if settings.debug:
        for k, v in settings.dict().items():
            log.debug(f"{k:10}: {v}")

    uvicorn.run(
        'app:app',
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
