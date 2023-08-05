from stylelens_index.database_image import DataBaseImage

class IndexImages(DataBaseImage):
  def __init__(self):
    super().__init__()
    self.images = self.db.images

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
                  offset=0, limit=10):
    query = {}
    query['version_id'] = version_id

    try:
      r = self.images.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)
