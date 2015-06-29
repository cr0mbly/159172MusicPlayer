import threading
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from musicPLayerAPI import Commands

class GUI:
    def __init__(self,root):
        #placeholder library list
        self.library = []


        #configure row/cols
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1,weight=1)
        root.rowconfigure(2,weight=1)

        #instaciate GUI elements
        self.player = Commands()
        self.menubar = Menu(root)
        self.playListBox = Listbox(root)
        self.libraryBox = Listbox(root)
        self.playListLabel = Label(root, text="Playlists")
        self.newPlaylist = Button(root, text = "New playlist")
        self.libraryLabel = Label(root, text="Library")
        self.albArtCanvas = Canvas(root, bg="yellow", height=150,width=150)
        self.queue = Listbox(root)
        self.photo = ImageTk.PhotoImage(file = "defaultImage.png")
        self.songString = StringVar()
        self.songString.set("title\nartist\nalbum")
        self.songInfo = Label(root, textvariable=self.songString, justify= LEFT)
        self.currentImg = self.albArtCanvas.create_image(0, 0, image=self.photo, anchor=NE)
        self.musicControl = Frame(root)
        self.previoustrack = Button(self.musicControl, text="prev")
        self.playToggle = Button(self.musicControl, text="play/pause", command=self.player.playPause)
        self.nextTrack = Button(self.musicControl, text="next")
        self.filemenu = Menu(self.menubar, tearoff=0)

        #configure GUI element positions

        self.libraryLabel.grid(row=0,column=1, sticky=W)
        self.playListBox.grid(row=1, column=0, sticky=N+S, rowspan=4)
        self.libraryBox.grid(row=1, column=1, sticky=N+S+E+W, rowspan=5)
        self.playListLabel.grid(row=0,column=0, sticky=W)
        self.newPlaylist.grid(row=3,column=0, sticky=W)
        self.albArtCanvas.grid(row=0,column=2, sticky=N+E, rowspan=4)
        self.songInfo.grid(row=1,column=2, sticky=S+W, pady=(25,0))
        self.previoustrack.grid(row=0, column=0)
        self.playToggle.grid(row=0,column=1)
        self.nextTrack.grid(row=0, column=2)
        self.musicControl.grid(row=3,column=2, sticky=N+W+E)
        self.queue.grid(row=2,column = 2, sticky=N+S+E+W)

        #Instanciate menu bar
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="load library", command=self.getlibrary)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)

        # bind functions to GUI elements

        self.libraryBox.bind('<<ListboxSelect>>', self.trackSelection)
        self.queue.bind('<<ListboxSelect>>', self.trackSelection)
        root.resizable(width=FALSE, height=FALSE)
        root.geometry('{}x{}'.format(800, 500))
        root.config(menu=self.menubar)


    def getlibrary(self):
        # get directory of library also starts companion thread to check if a track has finished

        self.library = self.player.loadLibarary(filedialog.askdirectory())
        self.player.queue = self.library
        for i in self.library:

            self.libraryBox.insert(END, i.title)
        songCheck = threading.Thread(target=self.songCheck)
        songCheck.start()

    def trackSelection(self,event):
        # plays the currently selected track from library

        w = event.widget
        index = int(w.curselection()[0])
        self.updateQueue()
        self.playtrack(self.library[index])

    def songCheck(self):
        # seperate thread that checks if a song has finished playing
            # TODO
        while True:
            if self.player.songFinished and len(self.player.queue)!= 0:
                print("in")
                self.playtrack(self.player.play(self.player.queue[0]))
                self.player.songFinished = False

    def updateQueue(self):
        # update queue when a song has finished or playlist is loaded
            # TODO

        self.player.queue.clear()
        for i in self.player.queue:

            self.queue.insert(END, i.title)
            root.update()





    def playtrack(self,track):
        #play track and update GUI

        strip = lambda string: string if len(string) <=20 else string[0:20]+ "..."
        self.photo = ImageTk.PhotoImage(track.image)
        self.songString.set( strip(track.title) + "\n" + strip(track.artist) + "\n" + strip(track.album))
        self.albArtCanvas.itemconfigure(self.currentImg, image=self.photo)
        self.player.play(track)
        root.update()





# intilise program
root = Tk()
GUI(root)
root.mainloop()