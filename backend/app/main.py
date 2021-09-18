import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from settings import config
from databases.db import Session
from starlette.requests import Request
import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware
from api.routers import v1


# ++++++++++++++++++++++++++++++++++++++++++++ DEFINE APP +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")


# ++++++++++++++++++++++++++++++++++++++++++++ HANDLE LOG FILE +++++++++++++++++++++++++++++++++++++++++++++++++++++++
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('logs/golang.log', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# ++++++++++++++++++++++++++++++++++++++++++++ ROUTER CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
app.include_router(v1.router, prefix="/api/v1")


# ++++++++++++++++++++++++++++++++++++++++++++ CORS MIDDLEWARE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
origins = [
    "http://{host}".format(host=config.HOST_NAME),
    "http://{host}:{port}".format(host=config.HOST_NAME, port = config.BE_PORT),
    "http://{host}:{port}".format(host=config.HOST_NAME, port = config.FE_PORT),
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ++++++++++++++++++++++++++++++++++++++++++++++ DB CONFIG ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# ++++++++++++++++++++++++++++++++++++++++++++++ RUN SERVICE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
    from worker import ml
    uvicorn.run(app, host='0.0.0.0',port=config.BE_PORT,debug=True)
