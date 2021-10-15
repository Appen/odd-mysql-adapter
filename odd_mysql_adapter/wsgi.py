import logging
import os

from flask_compress import Compress
from odd_contract import init_flask_app, init_controller

from .adapter import MysqlAdapter
from .cache import Cache
from .config import log_env_vars
from .controllers import Controller
from .scheduler import Scheduler

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)


def create_app(conf):
    app = init_flask_app()
    app.config.from_object(conf)
    log_env_vars(app.config)

    Compress().init_app(app)

    cache = Cache()
    adapter = MysqlAdapter(app.config)
    init_controller(Controller(adapter, cache))

    with app.app_context():
        Scheduler(adapter, cache).start_scheduler(int(app.config['SCHEDULER_INTERVAL_MINUTES']))
        return app


if os.environ.get('FLASK_ENVIRONMENT') == "production":
    application = create_app('odd_mysql_adapter.config.ProductionConfig')
else:
    application = create_app('odd_mysql_adapter.config.DevelopmentConfig')