import config
from app import init_app
from flask import Flask

import config


app = init_app()

if __name__ == "__main__":
    app.run(port = config.port, debug = True)