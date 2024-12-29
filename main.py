import logging
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from containers import Container
from note.interface.controllers.note_controller import router as note_routers
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.container = Container()

app.include_router(user_routers)
app.include_router(note_routers)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

@app.get("/")
def hello():
  return {"Hello": "FastAPI"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
  return JSONResponse(status_code=400, content=exc.errors(),)

@app.middleware("http")
async def http_middleware(request: Request, call_next):
  # 요청 정보
  method = request.method
  url = str(request.url)
  http_version = request.scope.get("http_version", "1.1")

  start_time = time.time()
  # 미들웨어가 여러 개 등록돼 있다면 다음 미들웨어로 전달하거나 엔드 포인트 함수로 요청을 전달한다.
  response = await call_next(request)

  status_code = response.status_code
  logging.info(f"{method} {url} HTTP/{http_version} {status_code}")

  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)

  return response