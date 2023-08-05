from stylelens_index.database import DataBase

class Indexes(DataBase):
  def __init__(self):
    super().__init__()
    self.images = self.db.images
    self.objects = self.db.objects

  def add_image(self, image):
    id = None
    try:
      query = {"host_code": image['host_code'],
               "product_no": image['product_no'],
               "version_id": image['version_id']}
      r = self.images.update_one(query,
                                 {"$set":image},
                                 upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

  def get_images(self, version_id,
                  sort_key=None,
                  sort_order=None,
                  offset=0, limit=10):
    query = {}
    query['version_id'] = version_id

    try:
      if sort_key is None:
        r = self.objects.find(query).skip(offset).limit(limit)
      else:
        r = self.objects.find(query).sort(sort_key, sort_order).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  def add_object(self, object):
    id = None
    try:
      query = {"name": object['name'],
               "version_id": object['version_id']}
      r = self.objects.update_one(query,
                                  {"$set":object},
                                  upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

  def get_objects(self, version_id,
                  sort_key=None,
                  sort_order=None,
                  offset=0, limit=10):
    query = {}
    query['version_id'] = version_id

    try:
      if sort_key is None:
        r = self.objects.find(query).skip(offset).limit(limit)
      else:
        r = self.objects.find(query).sort(sort_key, sort_order).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)

  # def get_images_by_object(self, object_id, offset=0, limit=100):
  #   query = {'_id'}
  #
  #   try:
  #     r = self.objects.find({query}).skip(offset).limit(limit)
  #
  #   except Exception as e:
  #     print(e)
  #
  #   return list(r)
