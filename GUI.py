__author__ = 'adhoulih'


import os
import threading
from Tkinter import *
import tkFileDialog
import functools

from PIL import ImageTk

from musicPLayerAPI import Commands
from linkedList import Node, SingleList


class GUI:
    def __init__(self, root):
        # lists containing library and playlist names
        self.library = []
        self.playlists = []

        # currently selected listbox elements
        self.currLibrIndex = 0
        self.curPListIndex = 0

        # variable containing song finished check
        self.currPlayThread = None

        # user terminated boolean
        self.exitFlag = False

        # configure row/cols
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        # instantiate GUI elements
        self.player = Commands()
        self.menuBar = Menu(root)

        self.queuePopup = Menu(root, tearoff=False)
        self.appendMenu = Menu(root, tearoff=False)
        self.mergeMenu = Menu(root, tearoff=False)
        self.queuePopup.add_cascade(label="append to playlist", menu=self.appendMenu)
        self.queuePopup.add_cascade(label="merge to playlist", menu=self.mergeMenu)

        self.popup = Menu(root, tearoff=False)
        self.playListMenu = Menu(root)
        self.popup.add_cascade(label="add to playlist", menu=self.playListMenu)
        self.popupFrame = Frame(root)

        self.playListBox = Listbox(root)
        self.libraryBox = Listbox(root)
        self.playListLabel = Label(root, text="Playlists")
        self.newPlaylist = Button(root, text="New playlist")
        self.libraryLabel = Label(root, text="Library")
        self.albArtCanvas = Canvas(root, height=150, width=150)
        self.queue = Listbox(root)
        self.photo = ImageTk.PhotoImage(file="defaultImage.png")
        self.songString = StringVar()
        self.songString.set("title\nartist\nalbum")
        self.songInfo = Label(root, textvariable=self.songString, justify=LEFT)
        self.currentImg = self.albArtCanvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.musicControl = Frame(root)
        self.shuffle = Button(self.musicControl, text="Shuffle")
        self.playToggle = Button(self.musicControl, text="play/pause", command=self.playtrack)
        self.nextTrack = Button(self.musicControl, text="next", command=self.playNext)
        self.filemenu = Menu(self.menuBar, tearoff=0)

        # configure GUI element positions

        self.libraryLabel.grid(row=0, column=1, sticky=W)
        self.playListBox.grid(row=1, column=0, sticky=N + S, rowspan=4)
        self.libraryBox.grid(row=1, column=1, sticky=N + S + E + W, rowspan=5)
        self.playListLabel.grid(row=0, column=0, sticky=W)
        self.newPlaylist.grid(row=3, column=0, sticky=W)
        self.albArtCanvas.grid(row=0, column=2, sticky=N + E, rowspan=4)
        self.songInfo.grid(row=1, column=2, sticky=S + W, pady=(25, 0))
        self.shuffle.grid(row=0, column=0)
        self.playToggle.grid(row=0, column=1)
        self.nextTrack.grid(row=0, column=2)
        self.musicControl.grid(row=3, column=2, sticky=N + W + E)
        self.queue.grid(row=2, column=2, sticky=N + S + E + W)


        # Instanciate menu bar
        self.menuBar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="load library", command=self.getlibrary)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)

        # bind functions to GUI elements
        self.shuffle.bind("<Button-1>", self.shufflePlist)
        self.playListBox.bind("<Button-3>", self.showQueueMenu)
        self.popup.bind('<<MENU-SELECT>>', self.addToPlayList)
        self.mergeMenu.bind('<<MENU-SELECT>>', self.mergePlist)
        self.appendMenu.bind('<<MENU-SELECT>>', self.appendPlist)
        self.playListBox.bind('<Double-Button-1>', self.loadPlayList)
        self.libraryBox.bind("<Button-3>", self.showLibraryMenu)
        self.newPlaylist.bind("<Button-1>", self.createPlayList)

        #set windows properties
        root.resizable(width=FALSE, height=FALSE)
        root.geometry('{}x{}'.format(800, 500))
        root.config(menu=self.menuBar)
        root.protocol("WM_DELETE_WINDOW", self.cleanup())


        self.initSession()

    def initSession(self):
        """
            load and initialise previous session

            :return: None
        """
        if os.path.isfile("tracks.lib"):
            file = open("tracks.lib", "r")
            for i in file.readlines():
                self.library.append(i)

                self.libraryBox.insert(END, Node(i, None).title)
        index = 0
        for file in os.listdir(os.getcwd()):
            if file.endswith(".pList"):
                fileName = os.path.splitext(os.path.basename(file))[0]
                self.playListBox.insert(END, fileName)
                self.playListMenu.add_command(label=fileName,
                                              command= functools.partial(self.addToPlayList,
                                                                                parent=self.playListMenu, index=index + 1))
                self.appendMenu.add_command(label=fileName,
                                              command=functools.partial(self.appendPlist, parent=self.appendMenu, index=index))


                self.mergeMenu.add_command(label=fileName,
                                              command=functools.partial(self.mergePlist, parent=self.mergeMenu, index=index))
                index += 1




    def createPlayList(self, event):
        """
            create and display new playlist

            :param event: object that called the function
            :return: None
        """

        pop = popupWindow(root)
        root.wait_window(pop.top)
        name = pop.value
        self.playlists.append(name)
        self.playListBox.insert(END, name)
        self.playListBox.update()
        playListName = name + ".pList"
        file = open(playListName, "a")
        file.close()

        index = self.playListMenu.index('last')
        self.playListMenu.add_command(label=name,
                                      command=lambda: self.addToPlayList(self.playListMenu, index))

    def addToPlayList(self, parent, index, multiNode=None):
        """
            add item or series of items to a playlist

            :param parent: menu container for current element
            :param index:  element index
            :param multiNode: optional param adds multiNode if used
            :return: None
        """

        with open(parent.entrycget(index, 'label') + ".pList", "w") as pList:
            if multiNode == None:
                pList.write(self.library[self.currLibrIndex])
            else:
                currentNode = multiNode.head
                while currentNode != None:
                    pList.write(currentNode.location + "\n")
                    currentNode = currentNode.next

    def loadPlayList(self, event):
        """
            load playList from file based on user selection

            :param event: object that called the function
            :return: None
        """

        self.player.linkedListQueue = SingleList()
        self.queue.delete(0, END)
        self.player.pygame.mixer.music.stop()
        if self.playListBox.size() > 0:
            w = event.widget
            index = int(w.curselection()[0])

            x = self.playListBox.get(index)
            self.curPlayList = x
            file = open(x + ".pList", 'r')
            for location in file.readlines():
                node = Node(location, None)
                self.queue.insert(0, node.title)
                self.player.linkedListQueue.addNode(node)

            self.currPlayThread = threading.Thread(target=self.songCheck)
            self.currPlayThread.start()




    def mergePlist(self, parent, index):

        """
            merge two user selected playlists together

            :param parent: menu container for current element
            :param index: element index
            :return: None
        """

        currentPList = self.player.loadPlistSelf(self.playListBox.get(self.curPListIndex))
        mergePList = self.player.loadPlistSelf(parent.entrycget(index, 'label'))
        currentPList.head = currentPList.mergePList(currentPList.head, mergePList.head)
        c = currentPList.head
        while c.next != None:
            c= c.next
            print c.location
        self.reloadQueue()
        self.addToPlayList(self.appendMenu, index, currentPList)


    def appendPlist(self, parent, index):
        """
            append two user selected playlists together

            :param parent: menu container for current element
            :param index: element index
            :return: None
        """


        currentPlist = self.player.loadPlistSelf(self.playListBox.get(self.curPListIndex))
        appendPlist = self.player.loadPlistSelf(parent.entrycget(index, 'label'))

        currentPlist.append(appendPlist.head)
        self.reloadQueue()
        self.addToPlayList(self.appendMenu, index, currentPlist)

    def reloadQueue(self):
        """
            update queue with current linkedList queue

            :return: None
        """

        self.queue.delete(0, END)
        currentNode = self.player.linkedListQueue.head
        while currentNode != None:
            self.queue.insert(END, currentNode.title)
            currentNode = currentNode.next

    def showLibraryMenu(self, event):
        """
            initialise and open library menu to add to playlist

            :return: None
        """

        widget = event.widget
        self.currLibrIndex = widget.nearest(event.y)
        self.popup.post(event.x_root, event.y_root)

    def showQueueMenu(self, event):
        """
            initialise and open queue menu containing options to append and update playlist

            :return: None
        """

        widget = event.widget
        self.curPListIndex = widget.nearest(event.y)
        self.queuePopup.post(event.x_root, event.y_root)

    def shufflePlist(self, event):
        """
            update and display a shuffled playlist

            :return: None
        """

        self.player.linkedListQueue.shuffle()
        self.reloadQueue()

    def getlibrary(self):
        """
            loads library into library listbox

            :return: None
        """

        loadedTracks = self.player.loadLibarary(tkFileDialog.askdirectory())
        for i in loadedTracks:
            self.libraryBox.insert(END, i.title)

    def songCheck(self):
        """
            function running on a different thread to check if song has finished

            :return: None
        """
        # seperate thread that checks if a song has finished playing
        while not self.exitFlag:
            for event in self.player.pygame.event.get():
                if event.type == self.player.pygame.USEREVENT:
                    self.updateQueue()
                    self.playtrack()

    def updateQueue(self):
        """
            update the queue with the current linkedList state

            :return: None
        """

        self.queue.delete(0, END)
        self.player.linkedListQueue.remove(0)

        currentItem = self.player.linkedListQueue.head

        while currentItem is not None:
            self.queue.insert(END, currentItem.title)
            currentItem = currentItem.next

        root.update()

    def playtrack(self):
        """
            play track and update GUI

            :return: None
        """


        track = self.player.linkedListQueue.head

        if not self.player.pygame.mixer.music.get_busy() and track is not None:
            strip = lambda string: string if len(string) <= 20 else string[0:20] + "..."
            self.photo = ImageTk.PhotoImage(track.image)
            self.songString.set(strip(track.title) + "\n" + strip(track.artist) + "\n" + strip(track.album))
            self.albArtCanvas.itemconfigure(self.currentImg, image=self.photo)

        self.player.playPause()
        root.update()

    def playNext(self):
        """
            plays the next track in the linkedlist

            :return: None
        """

        self.updateQueue()

        if self.player.linkedListQueue.head is not None:
            self.player.pygame.mixer.music.stop()
            self.playtrack()
        else:
            self.player.pygame.mixer.music.stop()

    def cleanup(self):
        """
            terminates running thread and program on user exit

            :return: None
        """

        self.exitFlag = True


class popupWindow(object):
    """
        popup windows for creating new playList
    """

    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.label = Label(top, text="new playlist name:")
        self.label.grid(row=0, column=0)
        self.playListName = Entry(top)
        self.playListName.grid(row=0, column=1)
        self.submit = Button(top, text='name Playlist', command=self.cleanup)
        self.submit.grid(row=1, column=0)

    def cleanup(self):
        """
            destroys window on close

            :return: None
        """

        self.value = self.playListName.get()
        self.top.destroy()

# intilise program
root = Tk()
GUI(root)
root.mainloop()
