import os
from pymongo import MongoClient

DB_HOST = os.environ['DB_USER_LOG_HOST']
DB_PORT = os.environ['DB_USER_LOG_PORT']
DB_NAME = os.environ['DB_USER_LOG_NAME']
DB_USER = os.environ['DB_USER_LOG_USER']
DB_PASSWORD = os.environ['DB_USER_LOG_PASSWORD']


class DataBaseUserLog(object):
  def __init__(self):
    self.client = MongoClient('mongodb://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT)
    self.db = self.client[DB_NAME]



