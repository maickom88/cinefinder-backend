import uvicorn

from src.config.config_app import init_app
from src.config.enviroment import env

if __name__ == "__main__":
    app = init_app()

    uvicorn.run(app,
                host=env.api_host(),
                port=env.api_port(),
                debug=env.is_debug()
                )
