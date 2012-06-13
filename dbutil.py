import pymongo
from gridfs import GridFS

class DB(pymongo.database.Database):
    conn = pymongo.Connection()
    RINGTONE_TYPE = 1
    def __init__(self,dbtype = "ordinary"):
        d_ = {
            "ordinary":"grat_compaign",
            "test":"grat_compaign_test",
            "file":"grat_files"
        }
        dbname = d_.get(dbtype,"grat_compaign_test")
        pymongo.database.Database.__init__(self,DB.conn,dbname)

        self.gridfs = GridFS(self)

    def save_tone_to_mongo(self,thing2read,filename):
        print self.gridfs.put(thing2read , filename = filename,type = DB.RINGTONE_TYPE )
        print "% saved to db" %filename

    def get_files(self,criteria):
        obj = self.fs.files.find(criteria)
        return obj

    def get_all_tone_ids(self):
        tone_ids = list()
        for t in self.get_files({"type":DB.RINGTONE_TYPE}):
            tone_ids.append((t["_id"],t["filename"]))
        print "%d tones" %(len(tone_ids))
        return tone_ids
    def get_tone(self,oid):
        fo = self.gridfs.get(oid)
        fp = "/home/xiaohan/Desktop/tmp.tone.mp3"
        with open(fp , "w") as f:
            f.write(fo.read())
        return fp            



            
db = DB()
