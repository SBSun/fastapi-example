import logging
import time

from fastapi import FastAPI, Request

from common.auth import CurrentUser, decode_access_token
from common.logger import logger
from context_var import user_context


def create_middlewares(app: FastAPI):
    @app.middleware("http")
    def get_current_user_middleware(request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            splits = authorization.split(" ")
            if splits[0] == "Bearer":
                token = splits[1]
                payload = decode_access_token(token)
                user_id = payload.get("user_id")
                user_role = payload.get("role")

                user_context.set(CurrentUser(user_id, user_role).__str__())

        logger.info(request.url)

        response = call_next(request)
        return response

    @app.middleware("http")
    async def get_api_execution_time_middleware(request: Request, call_next):
        # 요청 정보
        method = request.method
        url = str(request.url)
        http_version = request.scope.get("http_version", "1.1")

        start_time = time.time()
        # 미들웨어가 여러 개 등록돼 있다면 다음 미들웨어로 전달하거나 엔드 포인트 함수로 요청을 전달한다.
        response = await call_next(request)

        status_code = response.status_code
        process_time = time.time() - start_time

        logging.info(f"{method} {url} HTTP/{http_version} {status_code} {process_time}")

        response.headers["X-Process-Time"] = str(process_time)

        return response