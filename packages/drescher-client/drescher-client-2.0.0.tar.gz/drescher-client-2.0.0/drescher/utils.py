# coding: utf-8

from datetime import datetime
from uuid import UUID


def to_date(date_string, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(date_string, format)


def to_uuid(hex):
    return UUID(hex)
