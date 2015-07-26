__author__ = 'adhoulih'


"""
    API for interfacing with tracks
"""

import os
import pygame
from linkedList import *


class Commands:
    def __init__(self):
        self.library = []
        self.pygame = pygame
        self.linkedListQueue = SingleList()

        # user event to check if there is a next in queue
        self.nextInQueue = self.pygame.USEREVENT

        # program state booleans
        self.paused = False
        self.songFinished = None

        # pygame initializer
        self.pygame.init()

        # pygame music initializer
        self.pygame.mixer.init()
        self.pygame.mixer.music.set_endevent(self.nextInQueue)

    def playPause(self):
        """
            toggle play/pause
            :return: None
        """

        # toggle play/pause
        if not self.pygame.mixer.music.get_busy():
            self.play(self.linkedListQueue.head)
            return
        elif self.paused:
            self.pygame.mixer.music.unpause()
        else:
            self.pygame.mixer.music.pause()
        self.paused = not self.paused

    def play(self, track):
        """
            play track from start
        :param track: Node containing track info
        :return: None
        """

        self.pygame.mixer.music.load(track.location)
        while not self.pygame.mixer.music.get_busy():
            self.pygame.mixer.music.play()

    def loadLibarary(self, path):
        """
            load library from directory (checks subdirectories as well)
        :param path: library directory
        :return: list containing library nodes
        """
        with open("tracks.lib", "w+") as libFile:
            for root, dirs, files in os.walk(path):
                for f in files:
                    filename = os.path.join(root, f)
                    if filename.endswith('.mp3'):
                        libFile.write(filename + "\n")
                        self.library.append(Node(filename, None))
        return self.library

    def loadPlistSelf(self, location):
        """
            load a temporary playList into a linked list
        :param location: playlist file location
        :return: new linkedList playlist
        """

        file = open(location + ".pList", 'r')
        newPlist = SingleList()
        for location in file.readlines():
            node = Node(location, None)
            newPlist.addNode(node)
        return newPlist
