class Coordinates:
    def __init__(self,ra=50,level=1):
        self.radius = 50
        self.x = []
        self.y = []
        self.generateCoordinates(level)
        print("Coords: "+str(level))

    def generateCoordinates(self,level):
        if level==1:
            n=1
            for i in range(int(512/(self.radius*2))): # left column
                self.x.append(str(int(self.radius*n)))
                self.y.append(str(int(self.radius)))
                n = n+ 2
            n = 3
            for i in range(int((512-self.radius*2)/(self.radius*2))):  #top row
                self.x.append(str(int(self.radius*n)))
                self.y.append(str(int(self.radius)))
                n += 2
            n=3
            for i in range(int((512-self.radius*2)/(self.radius*2))):  #bottom row
                self.x.append(str(int(self.radius*n)))
                mult = int(1024/(self.radius*2))
                mult = mult*2
                self.y.append(str(int(self.radius)*mult))
                n += 2
            n = 3
            for i in range(int((1024-(self.radius*4))/(self.radius*2))):
                self.x.append(str(int(512-self.radius)))
                self.y.append(str(int(self.radius*n)))
                n += 2
        elif level==6:
            self.x.append(220)
            self.y.append(495)
        else:
            self.x.append(245)
            self.y.append(510)

