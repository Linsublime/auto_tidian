# coding=utf-8

import mongoengine as mg

MONGODB_SERVER = '192.168.0.43'
MONGODB_PORT = 27017

mgdb = mg.connect('oddsfair', host=MONGODB_SERVER, port=MONGODB_PORT, alias='od', maxPoolSize=2)


class TdContents(mg.EmbeddedDocument):
    type1 = mg.StringField()
    type2 = mg.StringField()
    type3 = mg.StringField()
    type4 = mg.StringField()
    type5 = mg.StringField()
    type6 = mg.StringField()
    type7 = mg.StringField()
    type8 = mg.StringField()
    type9 = mg.StringField()
    type10 = mg.StringField()
    gamebrief = mg.StringField()


class TidianContent(mg.Document):
    data_id = mg.IntField()
    contents = mg.EmbeddedDocumentField(TdContents, db_field='tidian')

    meta = {'collection': 'tidian_contents', 'db_alias': 'od'}
