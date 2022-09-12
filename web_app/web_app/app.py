from flask import Flask
from flask_injector import FlaskInjector
from main.main import setup_dependency_injection
from web_app.blueprints.auctions import AuctionsWeb


def create_app() -> Flask:
    app = Flask(__name__)

    FlaskInjector(
        app,
        modules=[AuctionsWeb()],
        injector=setup_dependency_injection(),
    )

    return app
