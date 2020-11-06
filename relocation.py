import guiControl 
import time
import coordinates as Coords


class Relocation:

    MOUSE_SPEED = 0.4
    COOLDOWN_TIME = 0.4
    

    def __init__(self,radius=50,level=1):
        self.x = []
        self.y = []
        self.current = 0
        self.failedPositions = [[0,0]]
        self.operations = [0,0,0,0] #left right up down
        self.COORDINATES = Coords.Coordinates(radius,level)
        self.fillCoordinates()
        self.GC = guiControl.guiControl(self.MOUSE_SPEED)

    def fillCoordinates(self):
        
        self.x = self.COORDINATES.x
        self.y = self.COORDINATES.y

    def moveFocusToLocation(self,x,y):
        
        self.coolDown()

        self.GC.openCoordinateLocator() 


        self.coolDown()

        self.GC.iXCoordinate(x)


        self.coolDown()


        self.GC.iYCoordinate(y)

        self.coolDown()

        self.GC.cGoButton()

        self.coolDown()



    def coolDown(self,cTime=0):
        if cTime!=0:
            time.sleep(cTime)
            return
        time.sleep(self.COOLDOWN_TIME)

    def relocateTown(self,x,y):
        self.moveFocusToLocation(x,y)
        while(not self.moveTown()):          
            coords = self.getNeighbour()
            self.moveFocusToLocation(coords[0],coords[1])


    def moveTown(self):    
        self.GC.cCentre()

        self.coolDown(1)

        if self.GC.isMyTown():
            self.GC.cExitButton()
            self.coolDown()
            return True

        if not self.GC.cApplyButton():
            self.coolDown(0.5)
            print(self.GC.cExitButton())
            return False
        else:
            self.coolDown()
            self.GC.cYesButton()
            self.coolDown()
            return True    

    def getNeighbour(self):
        currentPosition = [int(self.x[self.current]),int(self.y[self.current])]
        self.failedPositions.append(currentPosition)
        offset = 1
        newPosition = [0,0]

        while newPosition in self.failedPositions:
            if self.operations[0] == 0 :
                newPosition = [ currentPosition[0] - offset, currentPosition[1] ]
                self.operations[0] = 1
            elif self.operations[1] == 0 :
                newPosition = [ currentPosition[0] + offset, currentPosition[1] ]
                self.operations[1] = 1
            elif self.operations[2] == 0 :
                newPosition = [ currentPosition[0] , currentPosition[1] - (2*offset) ]
                self.operations[2] = 1
            elif self.operations[3] == 0 :
                newPosition = [ currentPosition[0] , currentPosition[1] + (2*offset) ]
                self.operations[3] = 1
            else:
                offset += 1
                for i in range(len(self.operations)):
                    self.operations[i] = 0

        return newPosition
