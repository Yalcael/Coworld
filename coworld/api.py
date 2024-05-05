from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from coworld.models.errors import BaseError
from coworld.routes.dishes import router as dishes_router
from coworld.routes.menus import router as menus_router
from coworld.routes.reservations import router as reservations_router


def create_app():
    app = FastAPI(title="Coworld API")
    app.include_router(dishes_router)
    app.include_router(menus_router)
    app.include_router(reservations_router)

    @app.exception_handler(BaseError)
    async def exception_handler(request: Request, exc: BaseError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "name": exc.name,
                "status_code": exc.status_code,
            },
        )

    return app
