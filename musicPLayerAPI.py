""" API for interfacing with tracks """
import io
import os
import threading

import pygame
from mutagen.mp3 import MP3
from PIL import Image
from pygame.constants import USEREVENT



#Music player API

class Commands:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.nextInQueue = USEREVENT + 1
        pygame.mixer.music.set_endevent(self.nextInQueue)

        self.queue = []
        self.pauseState = False
        self.songFinished = True


        #start event checking thread
        t = threading.Thread(target=self.checkEvents)
        t.start()


    def checkEvents(self):

        # seperate thread that checks if a certain event has happened
        while True:
            for e in pygame.event.get():
                if e.type == self.nextInQueue:
                    self.queue = self.queue[1:]
                    self.songFinished = True

    def playPause(self):
        # toggle play/pause

        if self.pauseState:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()
        self.pauseState = not self.pauseState

    def play(self,track):
        #play track from start

        pygame.mixer.music.stop()
        pygame.mixer.music.load(track.location)
        pygame.mixer.music.play()

    def loadPlayList(self, playFile):
        # load playlist from file
        file = open(playFile,'r')
        for i in file.readlines():
            self.queue.append(track(i))

    def loadLibarary(self, path):
        # load playlist from directory (checks subdirectories as well)
         with open("tracks.lib", "w+") as libFile:
            for root, dirs, files in os.walk(path):
               for f in files:
                   filename = os.path.join(root, f)
                   if filename.endswith('.mp3'):
                      libFile.write(filename)
                      self.queue.append(track(filename))
         return self.queue

    def nextTrack(self):
        return "TODO"

    def prevTrack(self):
        return "TODO"

class track:

    # track class that pulls out metadata from a mp3 file
    def __init__(self, location):
        trackFile = MP3(location)
        self.location = location
        self.title = trackFile['TIT2'].__dict__['text'][0]
        self.album = trackFile['TALB'].__dict__['text'][0]
        self.artist = trackFile['TPE1'].__dict__['text'][0]
        self.image = Image.open(io.BytesIO(trackFile["APIC:"].__dict__['data'])).resize((200,200), Image.ANTIALIAS)
