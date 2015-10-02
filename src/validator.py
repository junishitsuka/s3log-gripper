# coding: utf-8

import const
from datetime import datetime as dt

def collection_validate(collection):
    if collection in const.COLLECTION_LIST:
        return True

    return False

def date_validate(date):
    try:
        dt.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False

    return True
