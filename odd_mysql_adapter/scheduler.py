import logging
from datetime import datetime

import pytz
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from .adapter import MysqlAdapter
from .cache import Cache


class Scheduler:
    def __init__(self, adapter: MysqlAdapter, cache: Cache) -> None:
        self.__adapter = adapter
        self.__cache = cache
        self.__scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(1)})

    def start_scheduler(self, interval_minutes: int):
        self.__scheduler.start()
        self.__scheduler.add_job(self.__retrieve_data_entities,
                                 trigger='interval',
                                 minutes=interval_minutes,
                                 next_run_time=datetime.now(tz=pytz.UTC))

    def __retrieve_data_entities(self):
        datasets = self.__adapter.get_data_entities()
        self.__cache.cache_data_entities(datasets)
        logging.info(f'Put {len(datasets)} Datasets DataEntities to cache from database')
