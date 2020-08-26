import os
import sys

import elasticsearch
from flask import current_app, g
from tinydb import TinyDB, Query, operations

from archivy.config import Config

def get_db():
    if 'db' not in g:
        g.db = TinyDB(
            os.path.join(
                current_app.config['APP_PATH'],
                'db.json'
            )
        )

    return g.db


def get_max_id():
    db = get_db()
    max_id = db.search(Query().name == "max_id")
    if not max_id:
        db.insert({"name": "max_id", "val": 0})
        return 0
    return max_id[0]["val"]


def set_max_id(val):
    db = get_db()
    db.update(operations.set("val", val), Query().name == "max_id")


def elastic_client():
    if not Config.ELASTICSEARCH_ENABLED:
        return None
    es = elasticsearch.Elasticsearch([Config.ELASTICSEARCH_URL])
    try:
        health = es.cluster.health()
    except elasticsearch.exceptions.ConnectionError:
        sys.stderr.write(
            "Elasticsearch does not seem to be running on "
            f"{Config.ELASTICSEARCH_URL}. Please start "
            "it, for example with: sudo service elasticsearch restart\n"
        )
        sys.stderr.write(
            "You can disable Elasticsearch by setting the "
            "ELASTICSEARCH_ENABLED environment variable to 0\n"
        )
        sys.exit(1)

    if health["status"] not in ("yellow", "green"):
        sys.stderr.write(
            "WARNING: Elasticsearch reports that it is not working "
            "properly. Search might not work. You can disable "
            "Elasticsearch by setting ELASTICSEARCH_ENABLED to 0."
        )
    return es