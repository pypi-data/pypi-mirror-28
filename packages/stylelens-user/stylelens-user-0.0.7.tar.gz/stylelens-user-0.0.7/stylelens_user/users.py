from bson.objectid import ObjectId
from stylelens_user.database_user import DataBaseUser

class Users(DataBaseUser):
  def __init__(self):
    super(Users, self).__init__()
    self.users = self.db.users
    self.images = self.db.images
    self.objects = self.db.objects

  def add_user(self, user):
    query = {}

    query['device_id'] = user['device_id']

    try:
      r = self.users.update_one(query,
                                {"$set": user},
                                upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])
      return id
    else:
      return None

  def increase_user_profile_category(self, device_id, category):

    inc = {}
    inc['category.' + category] = 1
    try:
      r = self.users.update_one({"device_id": device_id},
                                  {"$inc": inc})
    except Exception as e:
      print(e)
      return None

    return r.raw_result

  def get_user_by_id(self, id):
    query = {}
    query['_id'] = ObjectId(id)
    try:
      r = self.users.find_one(query)
    except Exception as e:
      print(e)

    return r

  def get_user_by_device_id(self, id):
    query = {}
    query['device_id'] = id
    try:
      r = self.users.find_one(query)
    except Exception as e:
      print(e)

    return r

  def add_image(self, device_id, image):
    image['device_id'] = device_id

    try:
      r = self.images.insert(image)
    except Exception as e:
      print(e)
      return None

    return str(r)


  def get_image(self, image_id):
    query = {}
    query['_id'] = ObjectId(image_id)
    try:
      r = self.images.find_one(query)
    except Exception as e:
      print(e)
      return None

    return r

  def add_object(self, device_id, object):
    object['device_id'] = device_id

    try:
      r = self.objects.insert(object)
    except Exception as e:
      print(e)
      return None

    return str(r)

  def get_object(self, object_id):
    query = {}
    query['_id'] = ObjectId(object_id)
    try:
      r = self.objects.find_one(query)
    except Exception as e:
      print(e)
      return None

    return r

  def get_objects_by_image_id(self, image_id):
    query = {}
    query['image_id'] = image_id
    try:
      r = self.objects.find(query)
    except Exception as e:
      print(e)
      return None

    return r
