from bson.objectid import ObjectId
from stylelens_user.database_log import DataBaseUserLog

class UserLogs(DataBaseUserLog):
  def __init__(self):
    super(UserLogs, self).__init__()
    self.logs = self.db.logs

  def add_image_file_search_log(self, log):
    log['is_image_file_search'] = True

    if log.get('device_id', None) is None:
      print('Need a device_id')
      return None

    try:
      r = self.logs.insert(log)
    except Exception as e:
      print(e)
      return None

    if r is not None:
      return str(r)
    else:
      return None

  def add_image_index_search_log(self, log):
    log['is_image_index_search'] = True

    if log.get('device_id', None) is None:
      print('Need a device_id')
      return None

    try:
      r = self.logs.insert(log)
    except Exception as e:
      print(e)
      return None

    if r is not None:
      return str(r)
    else:
      return None

  def add_object_id_search_log(self, log):
    log['is_object_id_search'] = True

    if log.get('device_id', None) is None:
      print('Need a device_id')
      return None

    try:
      r = self.logs.insert(log)
    except Exception as e:
      print(e)
      return None

    if r is not None:
      return str(r)
    else:
      return None

  def get_image_file_search_images(self, offset=0, limit=10):
    query = {}
    query['is_image_file_search'] = True

    projection = {}
    projection['image_id'] = 1

    try:
      r = self.logs.find(query, projection).skip(offset).limit(limit)
    except Exception as e:
      print(e)
      return None

    return list(r)

  def get_image_file_search_logs(self, offset=0, limit=10):
    query = {}
    query['is_image_file_search'] = True

    try:
      r = self.logs.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)
      return None

    return list(r)

  def get_image_file_search_logs(self, offset=0, limit=10):
    query = {}
    query['is_image_file_search'] = True

    try:
      r = self.logs.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)
      return None

    return list(r)

  def get_image_index_search_logs(self, offset=0, limit=10):
    query = {}
    query['is_image_index_search'] = True

    try:
      r = self.logs.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)
      return None

    return list(r)

