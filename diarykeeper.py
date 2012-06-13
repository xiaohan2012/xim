from bean import BeanManager
from codecs import open
class Reader(object):
    def read(self,*args,**kwargs):
        return {}

class StdIOReader(Reader):
    def read(self):
        return ""

TXT_DIARY_PATH = "/home/xiaohan/Desktop/diary.txt"
class TextFileReader(Reader):
    def read(self):
        with open(TXT_DIARY_PATH,'r',"utf8") as f:
            events = []
            for l in f.readlines():
                if len(l.strip()) == 0:#meaningless
                    continue
                l = l.strip()
                bean_type,rest = l.split(":",1)
                content,tags_str = rest.split("##",1)
                tags = tags_str.strip().split("\t") if tags_str else None 
                print content,tags_str
                #print bean_type,content,tags
                events.append({
                    "bt":bean_type,
                    "content":content,
                    "tags":tags
                })

        #empty the text file        
        with open(TXT_DIARY_PATH,'w',"utf8") as f:                
            f.write("gratitude:\nreflection:\ngain:\n")
                
        return events

class ReaderFactory(object):

    @staticmethod
    def getReader(reader_type):
        r_d = {
            "std":StdIOReader,
            "txt":TextFileReader,
        }
        return r_d.get(reader_type,Reader)()

class DiaryKeeper(object):
    def collect_diary(self,diary_type):
        print "init reader"
        reader = ReaderFactory.getReader(diary_type)
        print "begin reading"
        beans = reader.read()
        bm = BeanManager()
        print "adding beans"
        for b in beans:
            print "adding",b
            bm.add_bean(**b)
    def clean_diary(self):
        bm = BeanManager()
        bm.clean_beans()

        
if __name__ == "__main__":
    dk = DiaryKeeper()
    dk.collect_diary("txt")
