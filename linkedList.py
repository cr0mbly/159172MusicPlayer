import io
import random
import copy
from PIL import Image
from mutagen.mp3 import MP3

__author__ = 'adhoulih'


class SingleList(object):
    def __init__(self):
        self.head = None

    def addNode(self, Node):
        """
            add a node to the linkedList
            :param Node: node to be added
            :return: None
        """

        currentNode = Node
        if self.head is None:
            self.head = currentNode
            self.head.next = None
        else:
            currentNode.next = self.head
            self.head = currentNode

    def remove(self, index):
        """
            remove node by index value
        :param index: index value
        :return: None
        """

        if index == 0:
            self.head = self.head.next
            return
        current_node = self.head
        previous_node = None
        counter = 0
        while current_node is not None:
            if counter == index:
                # if this is the first node (head)
                if previous_node is not None:
                    previous_node.next = current_node.next
                else:
                    self.head = current_node.next
            # needed for the next iteration
            previous_node = current_node
            current_node = current_node.next
            counter += 1

    def get(self, index):
        """
            get a node by its index value
        :param index: index value
        :return: Node
        """

        if self.head is None:
            return None

        current = self.head
        counter = 0
        while current is not None:
            if counter == index:
                return current
            current = current.next
            counter += 1

    def append(self, pListNode):
        """
            append two platLists together
        :param pListNode: playList to be appended
        :return: None
        """

        current = self.head
        if current:
            while current.next is not None:
                current = current.next
            current.next = pListNode
        else:
            self.head = pListNode

    def mergePList(self, head, pListNode):
        """
            :param head: head of first platList
            :param pListNode: head of second playList
            :return: merged playList
        """

        if head is None:
            return pListNode
        elif pListNode is None:
            return head
        else:
            head.next = self.mergePList(pListNode, head.next)
            return head

    def shuffle(self):
        """
            shuffle linkedList node into random order
            :return: None
        """


        current = self.head
        newList = SingleList()
        listLen = 0

        while current.next is not None:
            listLen += 1
            current = current.next

        current = SingleList()
        current.head = copy.deepcopy(self.head)

        while current.head is not None:
            randIndex = random.randint(0, listLen)

            newList.addNode(copy.deepcopy(current.get(randIndex)))
            current.remove(randIndex)

            listLen -= 1
        self.head = newList.head




class Node(object):
    def __init__(self, location, next):
        self.next = next
        self.location = location
        trackFile = MP3(location.strip("\n"))

        self.location = location.strip("\n")
        self.title = trackFile['TIT2'].__dict__['text'][0]
        self.album = trackFile['TALB'].__dict__['text'][0]
        self.artist = trackFile['TPE1'].__dict__['text'][0]
        self.image = Image.open(io.BytesIO(trackFile["APIC:"].__dict__['data'])).resize((150, 150), Image.ANTIALIAS)


