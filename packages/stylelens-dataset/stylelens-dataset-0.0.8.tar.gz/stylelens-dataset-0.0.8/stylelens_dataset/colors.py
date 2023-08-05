from bson.objectid import ObjectId
from stylelens_dataset.database import DataBase

class Colors(DataBase):
  def __init__(self):
    super(Colors, self).__init__()
    self.colors = self.db.colors

  def add_color(self, object):
    id = None
    try:
      r = self.colors.update_one({"file": object['file']},
                                  {"$set": object},
                                  upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

