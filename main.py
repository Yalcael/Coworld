import uvicorn
from coworld.api import create_app


app = create_app()


if __name__ == '__main__':
    uvicorn.run(app, port=7000)
