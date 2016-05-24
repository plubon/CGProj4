from math import sqrt, ceil


class Drawer():

    def __init__(self, img):
        self.img = img
        self.points = None
        self.octant = None

    def setdata(self, x1, y1, x2, y2):
        self.points = [(x1, self.img.height()-y1), (x2, self.img.height()-y2)]
        self.setoctant()

    def putpointscircle(self, point, center):
        for i in range(8):
            self.octant = i
            newpoint = self.getoutputpoint(point)
            self.putPixel((center[0] + newpoint[0], center[1] + newpoint[1]))

    def putpointxaolincircle(self, point, center, val):
        for i in range(8):
            self.octant = i
            newpoint = self.getoutputpoint(point)
            self.putpixel(center[0] + newpoint[0], center[1] + newpoint[1], val)

    def xaolinwuline(self, x1, y1, x2, y2):
        if x1 > x2:
            temp = x1
            x1 = x2
            x2 = temp
            temp = y1
            y1 = y2
            y2 = temp
        L = 255
        B = 0
        y = float(y1)
        x = x1
        m = (y2-y1)/float(abs(x2-x1))
        while x <= x2:
            c1 = int(L * (1 - (y % 1)) + B * (y % 1))
            c2 = int(B * (1 - (y % 1)) + L * (y % 1))
            self.putpixel(x, int(y), c1)
            self.putpixel(x, int(y)+1, c2)
            y += m
            x += 1

    def dfun(self, r, y):
        return ceil(sqrt((r ** 2) - (y ** 2))) - sqrt((r ** 2) - (y ** 2))

    def xaolinwuciricle(self, x1, y1, x2, y2):
        L = 255
        B = 0
        r = int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        x = r
        y = 0
        self.putpointxaolincircle((x, y), (x1, y1), L)
        while x > y:
            y += 1
            x = int(ceil(sqrt(r * r - y * y)))
            properX = x
            t = self.dfun(r, y)
            c2 = int(L * (1 - t) + B * t)
            c1 = int(B * (1 - t) + L * t)
            self.putpointxaolincircle((properX, y), (x1, y1), c2)
            self.putpointxaolincircle((properX + 1, y), (x1, y1), c1)

    def putpixel(self, x, y, val):
        self.img.put('#%02x%02x%02x' % val, (x, y))

    def circle(self, x1, y1, x2, y2):
        self.setdata(x1, y1, x2, y2)
        r = int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        y1 = self.img.height() - y1
        de = 3
        dse = 5 - 2 * r
        d = 1 - r
        x = 0
        y = r
        self.putpointscircle((x,y), (x1,y1))
        while y > x:
            if d < 0:
                d += de
                de += 2
                dse += 2
            else:
                d += dse
                de += 2
                dse += 4
                y -= 1
            x += 1
            self.putpointscircle((x, y), (x1, y1))


    def drawsymbresenham(self, x1, y1, x2, y2):
        self.setdata(x1, y1, x2, y2)
        dx = self.getinputpoint(1)[0] - self.getinputpoint(0)[0]
        dy = self.getinputpoint(1)[1] - self.getinputpoint(0)[1]
        d = 2 * dy - dx
        de = 2 * dy
        dne = 2 * (dy - dx)
        xf = self.getinputpoint(0)[0]
        yf = self.getinputpoint(0)[1]
        xb = self.getinputpoint(1)[0]
        yb = self.getinputpoint(1)[1]
        self.putPixel(self.getoutputpoint((xf, yf)))
        self.putPixel(self.getoutputpoint((xb, yb)))
        while xf < xb:
            xf += 1
            xb -= 1
            if d < 0:
                d += de
            else:
                d += dne
                yf += 1
                yb -= 1
            self.putPixel(self.getoutputpoint((xf, yf)))
            self.putPixel(self.getoutputpoint((xb, yb)))


    def setoctant(self):
        a = (self.points[1][1] - self.points[0][1])/float(self.points[1][0] - self.points[0][0])
        x1 = self.points[0][0]
        x2 = self.points[1][0]
        if a > 1:
            if x1 < x2:
                self.octant = 1
            else:
                self.octant = 5
        elif a > 0:
            if x1 < x2:
                self.octant = 0
            else:
                self.octant = 4
        elif a > -1:
            if x1 < x2:
                self.octant = 7
            else:
                self.octant = 3
        else:
            if x1 < x2:
                self.octant = 6
            else:
                self.octant = 2

    def getinputpoint(self, n):
        if self.octant == 0:
            return self.points[n]
        if self.octant == 1:
            return self.points[n][1], self.points[n][0]
        if self.octant == 2:
            return self.points[n][1], -self.points[n][0]
        if self.octant == 3:
            return -self.points[n][0], self.points[n][1]
        if self.octant == 4:
            return -self.points[n][0], -self.points[n][1]
        if self.octant == 5:
            return -self.points[n][1], -self.points[n][0]
        if self.octant == 6:
            return -self.points[n][1], self.points[n][0]
        if self.octant == 7:
            return self.points[n][0], -self.points[n][1]

    def getoutputpoint(self, point):
        if self.octant == 0:
            return point
        if self.octant == 1:
            return point[1], point[0]
        if self.octant == 2:
            return -point[1], point[0]
        if self.octant == 3:
            return -point[0], point[1]
        if self.octant == 4:
            return -point[0], -point[1]
        if self.octant == 5:
            return -point[1], -point[0]
        if self.octant == 6:
            return point[1], -point[0]
        if self.octant == 7:
            return point[0], -point[1]

    def putPixel(self, point):
        self.img.put("#000000", (point[0], self.img.height()-point[1]))