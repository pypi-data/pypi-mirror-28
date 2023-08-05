
from bson.objectid import ObjectId
from stylelens_object.database_feature import DataBaseFeature

class Features(DataBaseFeature):
  def __init__(self):
    super(Features, self).__init__()
    self.features = self.db.features

  def add_feature(self, feature, version_id=None):
    query = {}

    if version_id is not None:
      query['version_id'] = version_id

    query['object_id'] = feature['object_id']

    try:
      r = self.features.update_one(query,
                                  {"$set": feature},
                                  upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])
      return id
    else:
      return None

  def get_feature_by_object_id(self, object_id):
    query = {}

    query['object_id'] = object_id

    try:
      r = self.features.find_one(query)
    except Exception as e:
      print(e)

    return r

