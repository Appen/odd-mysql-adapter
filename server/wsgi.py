import os
import logging
from flask import Response
from odd_contract import init_flask_app, init_controller
from adapter.adapter import create_adapter
from app.cache import Cache
from app.controller import Controller
from app.scheduler import Scheduler
from config import log_env_vars

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)


def create_app(conf):
    app = init_flask_app()

    app.config.from_object(conf)
    log_env_vars(app.config)

    app.add_url_rule('/health', 'healthcheck', lambda: Response(status=200))

    cache = Cache()
    adapter = create_adapter(app.config['ODD_DATA_SOURCE_NAME'], app.config['ODD_DATA_SOURCE'], app.config)
    init_controller(Controller(adapter, cache))

    cache_refresh_interval: int = int(app.config['SCHEDULER_INTERVAL_MINUTES'])
    with app.app_context():
        Scheduler(adapter, cache).start_scheduler(cache_refresh_interval)
        return app


application = create_app(os.environ.get('FLASK_CONFIG') or 'config.DevelopmentConfig')
