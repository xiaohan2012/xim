from dbutil import db
from datetime import datetime
from bson.objectid import ObjectId
from urllib2 import urlopen

BEAN_NAME_MAP = {
    "grat":"gratitude",
    "gain":"gain",
    "refl":"reflection"
}
class BeanManager(object):
    REGULAR_BEANS = ("gratitude","gain","reflection","task","idea")
    FILE_BEANS = ("ring_tone",)

    @staticmethod
    def add_bean(**kwargs):
        bt = kwargs["bt"]
        del kwargs["bt"]

        if bt in BeanManager.REGULAR_BEANS:
            kwargs["when_created"] = datetime.now()
            print kwargs
            return db["%s_bean" %bt].save(kwargs)
        elif bt in ("ring_tone",):
            url = kwargs["url"]
            filename = kwargs["filename"]
            try:
                db.save_tone_to_mongo(urlopen(url) , filename)
            except urllib2.HTTPError:
                pass
            
    @staticmethod
    def modify_bean(**kwargs):
        bt = kwargs["bt"]
        del kwargs["bt"]
        oid = kwargs["oid"]
        del kwargs["oid"]
        db["%s_bean" %bt].update({"_id":ObjectId(oid)},{"$set":kwargs})
            

    @staticmethod
    def get_beans(kwargs):
        bt = kwargs["bt"]
        del kwargs["bt"]
        if bt in BeanManager.REGULAR_BEANS:
            return db["%s_bean" %bt].find(kwargs)
        elif bt in BeanManager.FILE_BEANS:
            return db.get_files(kwargs)


    @staticmethod
    def clean_beans():
        for dbname in db.collection_names():
            print dbname
            db[dbname].remove()
            
