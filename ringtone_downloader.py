from pyquery import PyQuery as pq
from urlparse import  urljoin,urlparse
import threading
from Queue import Queue
from datetime import datetime

from bean import BeanManager

tone_list_url = "http://game.3533.com/lingsheng/6/4.htm"
RING_TONE_DB = "ring_tones"

def get_base_url(url):
    u = urlparse(url)
    return "%s://%s" %(u.scheme,u.hostname)

def get_tone_download_info(tone_list_url):
    doc = pq(tone_list_url)
    tone_links = doc.find(".td_padding a")
    base_url = get_base_url(tone_list_url)
    for tl in tone_links:
        tl = pq(tl)
        sub_url = urljoin(base_url,tl.attr('href'))
        name = tl.text()
        yield sub_url,name


def download_tone(url,tone_name):
    doc = pq(url)
    download_url = pq(doc.find("a#xiazai")[0]).attr("href")
    BeanManager.add_bean(bt = "ring_tone" , url = download_url , filename = tone_name)

class DownloadThread(threading.Thread):
    def __init__(self,name,queue):
        threading.Thread.__init__(self)
        self.q = queue
        self.name = name

    def run(self):
        while True:
            url,tone_name= self.q.get()

            doc = pq(url)
            download_url = pq(doc.find("a#xiazai")[0]).attr("href")
            BeanManager.add_bean(bt = "ring_tone" , url = url , filename = tone_name)

            self.q.task_done()
            print "I am robot %s, %s done" %(self.name , tone_name)

if __name__ == "__main__":
    q = Queue()
    for  t in get_tone_download_info(tone_list_url):
        q.put(t)

    start = datetime.now() 
    print "download begin"
    for i in xrange(10):
        t = DownloadThread(i , q)
        t.start()
    q.join()
    print "download done. %s s elapsed" %(datetime.now() - start)
