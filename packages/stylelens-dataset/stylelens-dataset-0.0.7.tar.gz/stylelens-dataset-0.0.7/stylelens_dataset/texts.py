from bson.objectid import ObjectId
from stylelens_dataset.database import DataBase

class Texts(DataBase):
  def __init__(self):
    super(Texts, self).__init__()
    self.texts = self.db.texts

  def add_texts(self, text_dataset):
    id = None
    query = {"class_code": text_dataset["class_code"], "text": text_dataset["text"]}
    try:
      r = self.texts.update_one(query, {"$set": text_dataset},upsert=True)
    except Exception as e:
      print(e)

    if 'upserted' in r.raw_result:
      id = str(r.raw_result['upserted'])

    return id

  def get_texts(self, class_code,  offset=0, limit=50):
    query = {"class_code": class_code}

    try:
      r = self.texts.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)