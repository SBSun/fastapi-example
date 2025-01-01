import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from containers import Container
from middlewares import create_middlewares
from note.interface.controllers.note_controller import router as note_routers
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.container = Container()

app.include_router(user_routers)
app.include_router(note_routers)

create_middlewares(app)

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s %(levelname)s: %(message)s"
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