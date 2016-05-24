import Tkinter as Tk
import tkFileDialog
from tkColorChooser import askcolor
from Drawer import Drawer
from math import sqrt, ceil
from ActiveEdgeTable import ActiveEdgeTable
from PIL import ImageTk, Image
from Queue import Queue

WIDTH = 800
HEIGHT = 800


class MainWindow(Tk.Tk):

    def __init__(self):
        Tk.Tk.__init__(self)
        self.filechooseoptions = self.getfilechooseoptions()
        self.toppanel = None
        self.botpanel = None
        self.canvas = None
        self.filter = None
        self.combobox = None
        self.neighs = None
        self.neighsVar = None
        self.img = None
        self.startX = None
        self.startY = None
        self.drawer = None
        self.color = (174,198,207)
        self.lastX = None
        self.lastY = None
        self.sorted = None
        self.image = None
        self.raster = None
        self.photo = None
        self.imageLabel = None
        self.currentFileName = None
        self.points = []
        self.initialize()

    def initialize(self):
        self.title = "CGP2"
        self.toppanel = Tk.Frame(self)
        self.toppanel.pack(side=Tk.TOP)
        Tk.Button(self.toppanel, text="Choose an image", command=self.fileselecthandler).pack(side=Tk.LEFT)
        self.botpanel = Tk.Frame(self)
        self.botpanel.pack()
        self.canvas = Tk.Canvas(self.botpanel, width=WIDTH, height=HEIGHT, bg='white')
        self.img = Tk.PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image((0, 0), image=self.img, anchor="nw")
        self.canvas.bind('<ButtonRelease-1>', self.onEnd)
        self.canvas.pack(fill=Tk.BOTH, expand=1)
        combooptions = ["Polygon Fill", "Region Fill"]
        neighOptions = [4, 8]
        self.neighsVar = Tk.StringVar(self)
        self.filter = Tk.StringVar(self)
        self.filter.set(combooptions[0])
        self.neighsVar.set(neighOptions[0])
        self.combobox = apply(Tk.OptionMenu, (self.toppanel, self.filter)+tuple(combooptions))
        self.combobox.pack(side=Tk.LEFT)
        self.neighs = apply(Tk.OptionMenu, (self.toppanel, self.neighsVar)+tuple(neighOptions))
        self.neighs.pack(side=Tk.LEFT)
        self.drawer = Drawer(self.img)
        Tk.Button(self.toppanel,text='Select Color', command=self.getColor).pack()
        self.mainloop()

    def polygon(self, event):
        if self.startX is None:
            self.startX = event.x
            self.startY = event.y
        else:
            if self.dist(event) < 30:
                self.sorted = sorted(self.points, key=lambda tup: tup[1], reverse=True)
                self.drawer.drawsymbresenham(self.startX, self.startY, self.lastX, self.lastY)
                self.fill()
            else:
                self.drawer.drawsymbresenham(self.lastX, self.lastY, event.x, event.y)
        self.points.append((event.x, event.y))
        self.lastX = event.x
        self.lastY = event.y

    def fill(self):
        n = len(self.points)
        k = 0
        ymax = self.sorted[0][1]
        ymin = self.sorted[len(self.sorted)-1][1]
        aet = ActiveEdgeTable()
        for y in range(ymax, ymin+1, -1):
            while k <= n and self.sorted[k][1] == y:
                i = self.points.index(self.sorted[k])
                if self.points[(i-1) % n][1] < self.points[i][1]:
                    aet.add(self.points[i][0], self.points[i][1], self.points[(i-1) % n][0], self.points[(i-1) % n][1])
                elif self.points[(i-1) % n][1] > self.points[i][1]:
                    aet.removeEdge(self.points[(i-1) % n][0], self.points[(i-1) % n][1], self.points[i][0], self.points[i][1])
                if self.points[(i + 1) % n][1] < self.points[i][1]:
                    aet.add(self.points[i][0], self.points[i][1], self.points[(i + 1) % n][0], self.points[(i + 1) % n][1])
                elif self.points[(i + 1) % n][1] > self.points[i][1]:
                    aet.removeEdge(self.points[(i + 1) % n][0], self.points[(i + 1) % n][1], self.points[i][0], self.points[i][1])
                k = k +1
            j = 0
            aet.sort()
            while(j <= len(aet.edges)-2):
                for xx in range(int(ceil(aet.edges[j].x)), int(round(aet.edges[j+1].x))):
                    self.drawer.putpixel(xx, y, self.color)
                j = j + 2
            aet.remove(y)
            aet.update()




    def dist(self, event):
        return sqrt((self.startX - event.x) ** 2 + (self.startY - event.y) ** 2)

    def onEnd(self, event):
        if self.filter.get() == "Polygon Fill":
            self.polygon(event)
        elif self.filter.get() == "Region Fill":
            self.region(event)

    def region(self, event):
        color = self.raster[event.x, event.y]
        print color
        q = Queue()
        visited = set()
        q.put((event.x, event.y), block=False)
        while not q.empty():
            px = q.get(block=False)
            visited.add(px)
            if self.colorDist(self.raster[px[0], px[1]], color) < 25:
                self.raster[px[0], px[1]] = self.color
                ns = self.getNs(px)
                for item in ns:
                    if item not in visited:
                        q.put(item)
        self.drawimage()

    def colorDist(self, c1, c2):
        x = 0
        for i in range(3):
            x += (c1[i] - c2[i]) ** 2
        return sqrt(x)

    def getNs(self, px):
        ret = []
        ret.append((px[0], px[1] + 1))
        ret.append((px[0], px[1] - 1))
        ret.append((px[0] - 1, px[1]))
        ret.append((px[0] + 1, px[1]))
        if self.neighsVar.get() == "8":
            ret.append((px[0] + 1, px[1] + 1))
            ret.append((px[0] + 1, px[1] - 1))
            ret.append((px[0] - 1, px[1] + 1))
            ret.append((px[0] - 1, px[1] - 1))
        return ret

    def getColor(self):
        color = askcolor()
        self.color = color[0]

    def fileselecthandler(self):
        self.currentFileName = tkFileDialog.askopenfilename(**self.filechooseoptions)
        if self.currentFileName:
            self.loadimage()

    def getfilechooseoptions(self):
        options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('jpg files', '.jpg'), ('all files', '.*')]
        options['initialdir'] = 'C:\\'
        options['title'] = 'Choose an image'
        return options

    def loadimage(self):
        self.image = Image.open(self.currentFileName)
        self.raster = self.image.load()
        self.drawimage()

    def drawimage(self):
        if self.photo is None and self.imageLabel is None:
            self.img = ImageTk.PhotoImage(self.image)
            self.raster = self.image.load()
            self.canvas.create_image((0, 0), image=self.img, anchor="nw")
        else:
            self.img = ImageTk.PhotoImage(self.image)
            self.raster = self.image.load()
            self.canvas.create_image((0, 0), image=self.img, anchor="nw")

if __name__ == "__main__":
    mw = MainWindow()