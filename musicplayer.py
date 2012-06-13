#!/usr/bin/env python
import pyaudio
import mad
import random 
import os
from StringIO import StringIO
import threading
import os

from dbutil import db

class Mp3Player(object):
    def load(self,fp):
        self.mf = mad.MadFile(fp)
        self.p = pyaudio.PyAudio()
        # open self.stream
        self.stream = self.p.open(format =
                        self.p.get_format_from_width(pyaudio.paInt32),
                        channels = 2,
                        rate = self.mf.samplerate(),
                        output = True)

    def play(self):
        # read data
        data = self.mf.read()

        # play self.stream
        while data != None:
            self.stream.write(data)
            data = self.mf.read()
            

class ToneMp3Player(Mp3Player):
    def random_select(self):
        tone_id,filename = random.choice(db.get_all_tone_ids())
        self.fp = db.get_tone(tone_id)
        print filename
        self.load(self.fp)

    def play(self):
        Mp3Player.play(self)
        os.remove(self.fp)

    def random_play(self):
        while True:
            try:
                self.random_select()
                self.play()
                break
            except IOError:            
                print "format incorrect"
                continue


def add_ringtone(action_list):
    def outter_wrapper(fun):
        def wrapper(self):
            self.fun()
            if attr in action_list and not os.fork():
                os.system('musicplayer.py')
                os._exit(0)
        return wrapper                
    return outter_wrapper

if __name__ == "__main__":
    p = ToneMp3Player()
    p.random_play()
