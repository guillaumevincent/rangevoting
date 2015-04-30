import sys
import logging

import pymongo
import pymongo.errors
import smartconfigparser

from repository import MongoRepository


logger = logging.getLogger(__name__)


def get_mongo_repository():
    config = smartconfigparser.Config()
    config.read('config.ini')
    host = config.get('DATABASE', 'host', 'localhost')
    port = config.getint('DATABASE', 'port', 27017)
    try:
        database = pymongo.MongoClient(host, port)['rangevoting']
        return MongoRepository(database)
    except (pymongo.errors.ConnectionFailure, pymongo.errors.AutoReconnect):
        logger.exception('mongo database is not started on mongodb://{0}:{1}/'.format(host, port))
        sys.exit(0)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s  %(name)12s %(levelname)7s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)