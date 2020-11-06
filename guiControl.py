import pyautogui
from imageProcessing import ImageRecognition
import os
import time
class guiControl:
    hasClosed = False

    def __init__(self,mouseSpeed):
        self.MOUSE_SPEED = mouseSpeed
        pyautogui.FAILSAFE = True
        self.iP = ImageRecognition()
        self.height = self.iP.getHeight()
        self.width = self.iP.getWidth()
        self.isFirst = True
        self.canClaimAll = True
        self.hasApplied = False
        self.hasEnteredTaskMenu = False
        
        self.invadersSlain = 0
        self.invaderType = "None"

    def fuseGems(self):
        waitP = 0.5
        applyCoord = []
        for i in range(50):
            if self.cTab(ImageRecognition.GEM):
                time.sleep(waitP)
                if self.cTab(ImageRecognition.FUSE):
                    time.sleep(waitP)
                    if self.cTab(ImageRecognition.FUSE2):
                        time.sleep(waitP)
                        if self.cTab(ImageRecognition.BOOST,1):
                            time.sleep(waitP)
                            self.scrollDown(10,0.2)
                            time.sleep(waitP)
                            while not self.cTab(ImageRecognition.FREE,1):
                                if len(applyCoord)==0:
                                    pyautogui.moveTo(x=400,y=400)
                                    if self.iP.isOnScreen(ImageRecognition.APPLY3H):
                                        applyCoord = self.iP.coordinates
                                        pyautogui.moveTo(applyCoord)
                                        pyautogui.click(applyCoord)
                                else:
                                    pyautogui.moveTo(applyCoord)
                                    pyautogui.click(applyCoord)
                            time.sleep(waitP)
                        elif self.cTab(ImageRecognition.FREE):
                            time.sleep(waitP)


    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width    

    def quitWindow(self):

        self.cCentre()
        pyautogui.keyDown('alt')
        pyautogui.keyDown('F4')
        time.sleep(0.3)
        pyautogui.keyUp('alt')
        pyautogui.keyUp('F4')
        time.sleep(1)

    def isLoaded(self):
        return self.iP.isOnScreen(ImageRecognition.VIKINGMENU)

    def isTask(self):
        if self.iP.isOnScreen(ImageRecognition.APPLY,2,0.1) or self.iP.isOnScreen(ImageRecognition.START,2,0.1):
            return True
        else:
            return False

    def completeTask(self,taskType):
        if not self.hasEnteredTaskMenu:
            if taskType == "Clan":
                self.iP.isOnScreen(ImageRecognition.CLANTASK,3,0.3,0.75)
                pyautogui.moveTo(self.iP.coordinates,duration=int(self.MOUSE_SPEED/4))
                pyautogui.click(self.iP.coordinates,clicks=2)
            elif taskType=="Premium":
                self.iP.isOnScreen(ImageRecognition.PREMIUMTASK,3,0.3,0.75)
                pyautogui.moveTo(self.iP.coordinates,duration=int(self.MOUSE_SPEED/4))
                pyautogui.click(self.iP.coordinates,clicks=2)
            self.hasEnteredTaskMenu = True

        time.sleep(0.5)
        if not self.doTask():
            return False
        else:
            return True

    def doTask(self):
        counter=0
        if self.hasApplied==False and self.iP.isOnScreen(ImageRecognition.APPLY,1,0.1):
            pyautogui.moveTo(self.iP.coordinates,duration=int(self.MOUSE_SPEED/4))
            pyautogui.click(self.iP.coordinates)
            self.hasApplied = True

        if self.canClaimAll and self.iP.isOnScreen(ImageRecognition.CLAIMALL,4,0.4):
            pyautogui.moveTo(self.iP.coordinates,duration=int(self.MOUSE_SPEED/4))
            pyautogui.click(self.iP.coordinates)
            self.canClaimAll = True
            self.hasApplied = False
            return True
        else:
            if not self.iP.isOnScreen(ImageRecognition.APPLY,1,0.1):
                self.canClaimAll = False

        while not self.iP.isOnScreen(ImageRecognition.TASKCOMPLETED) and not self.hasClosed:
            pyautogui.moveTo(x=(self.width/2), y=(self.height/2),duration=self.MOUSE_SPEED) 
            counter+=1
            startLocations = self.iP.getObjectsOnScreen(ImageRecognition.START,1,0,0.75)
            if startLocations==False:
                claimLocations = self.iP.getObjectsOnScreen(ImageRecognition.CLAIM)
                if claimLocations!=False:
                    for i in claimLocations:
                        pyautogui.moveTo(claimLocations[0],duration=int(self.MOUSE_SPEED/4))
                        pyautogui.click(claimLocations[0],duration=0.1)
                        time.sleep(0.1)
                    pyautogui.click(claimLocations[0])
                    pyautogui.click(claimLocations[0])
                else:
                    counter += 4
            else:
                for j in startLocations:
                    pyautogui.moveTo(j,duration=int(self.MOUSE_SPEED/4))
                    pyautogui.click(j,duration=0.15)
                pyautogui.click()
            if counter>=5:
                break
                return False
        self.hasApplied = False
        return True

    def changeTaskType(self):
        pass
    
    def taskManager(self):
        pyautogui.typewrite(['z'])
        print("Pressed Z")

    def openCoordinateLocator(self):
        pyautogui.press("n")

    def iXCoordinate(self,x):
        if self.iP.isOnScreen(self.iP.XINPUT):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)#x=617, y=475,duration=self.MOUSE_SPEED)     #type in x coordinate
        pyautogui.click()
        pyautogui.click()
        pyautogui.typewrite(str(x))
        return True

    def iYCoordinate(self,y,):
        if self.iP.isOnScreen(self.iP.YINPUT):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)#x=820, y=475,duration=self.MOUSE_SPEED)     #type in y coordinate
        pyautogui.click()
        pyautogui.click()
        pyautogui.typewrite(str(y))
        return True

    def cGoButton(self):
        if self.iP.isOnScreen(self.iP.GOTO):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)#x=830, y=596,duration=self.MOUSE_SPEED)     #click go to button
        pyautogui.click()
        return True
    
    def cCentre(self):
        pyautogui.moveTo(x=(self.width/2), y=(self.height/2),duration=self.MOUSE_SPEED)     #click centre of the screen
        pyautogui.click()
        return True

    def goToWebsite(self,browser,url=""):
        if self.hasClosed==True:
            return False
        os.startfile(browser)
        if self.hasClosed==True:
            return False
        time.sleep(1)
        if self.hasClosed==True:
            return False
        pyautogui.typewrite(url,interval=0.01)
        if self.hasClosed==True:
            return False
        return True

    def isLoggedIn(self):
        if self.iP.isOnScreen(self.iP.USERICON):
            return True
        else:
            return False

    def logOut(self):
        if self.iP.isOnScreen(self.iP.USERICON):
            coords = self.iP.coordinates
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        if self.iP.isOnScreen(self.iP.LOGOUT):
            coords2 = self.iP.coordinates
        pyautogui.moveTo(coords2,duration=self.MOUSE_SPEED)
        pyautogui.click()
        time.sleep(0.3)
        if self.iP.isOnScreen(self.iP.LOGOUTYES):
            coords3 = self.iP.coordinates
        pyautogui.moveTo(coords3,duration=self.MOUSE_SPEED)
        pyautogui.click()

    def logIn(self,email,password):
        self.cLogIn()
        time.sleep(0.5)

        if self.iP.isOnScreen(self.iP.EMAIL):
            coords = self.iP.coordinates
            coords = [coords[0],coords[1]+(self.height*0.05)]
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click(coords,clicks=3,interval=0.1)
        time.sleep(0.3)
        pyautogui.typewrite(email)

        time.sleep(0.3)
        coords = [coords[0],coords[1]+(self.height*0.09)]
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click(coords,clicks=3,interval=0.1)
        time.sleep(0.3)
        pyautogui.typewrite(password)

        time.sleep(0.2)

        if self.iP.isOnScreen(self.iP.USERLOGIN):
            coords = self.iP.coordinates
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click()
    
    def cPlayNow(self):
        if self.iP.isOnScreen(self.iP.PLAYNOW,10):
            coords = self.iP.coordinates
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click(coords,clicks=3,interval=0.3)

    def closePopUps(self,number):
        for i in range(number):
            if self.iP.isOnScreen(self.iP.EXIT):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                pyautogui.click()
            time.sleep(1)
    
    def oNavigator(self):
        pyautogui.typewrite('w')
        time.sleep(1)
        while not self.iP.isOnScreen(ImageRecognition.NAVIGATOR,4):
            self.cExitButton()
            pyautogui.typewrite('w')
            time.sleep(1)

    def oMap(self):
        time.sleep(1)
        pyautogui.typewrite('m')
        time.sleep(3)

    def selectLocationType(self,level):
        if not self.iP.isOnScreen(self.iP.LOCATIONTYPEINVADER):
            self.cTab(self.iP.SELECTLOCATIONTYPE)
            time.sleep(0.5)

            self.cTab(self.iP.INVADEROPTION)
        else:
            if not self.cTab(self.iP.SECONDMENU):
                self.cTab(self.iP.SECONDMENU2)
        time.sleep(0.5)

        if level==1:
            if self.iP.isOnScreen(self.iP.LEVEL1):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                pyautogui.click(coords)
                print("Level 1 selected")
        elif level==6:
            pyautogui.moveTo(x=20,y=20,duration=self.MOUSE_SPEED)
            if self.iP.isOnScreen(self.iP.LEVEL6):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                pyautogui.click(coords)
                print("Level 6 selected")
        elif level==7:
            pyautogui.moveTo(x=20,y=20,duration=self.MOUSE_SPEED)
            if self.iP.isOnScreen(self.iP.UBER):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                pyautogui.click(coords)
                print("Level Uber selected")

        time.sleep(0.5)
        self.cExitButton()
        time.sleep(0.5)

    def closeWindowCheckBox(self,value):
        if value:
            self.cTab(self.iP.CHECKBOX)
        else:
            self.cTab(self.iP.CHECKEDBOX)
            

    def killLevel1Invader(self):
        time.sleep(2)
        if self.iP.isOnScreen(self.iP.FIRSTINFO,10,0.4,0.95) or self.iP.isOnScreen(ImageRecognition.INFO):
            self.cTab(ImageRecognition.FIRSTINFO)
            if self.isFirst == True:
                self.closeWindowCheckBox(True)
                self.isFirst = False
        else:
            return False
        while not self.iP.isOnScreen(self.iP.ATTACKE):
            if self.hasClosed==True:
                break
            time.sleep(1)
        coords = self.iP.coordinates
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click()
        self.invadersSlain += 1
        return True

    def killInvaders(self):
        self.oNavigator()
        time.sleep(2)
        if self.invaderType=="None":
            self.locateInvader()
        else:
            self.locateSpecificInvader()
        while not self.moveNextToInvader():
            self.oNavigator()
            self.scrollDown(3)
            self.locateInvader()
        time.sleep(0.5)
        self.killInvader()
        self.invadersSlain += 1
        
    def killInvader(self):
        counter = 0
        time.sleep(2)
        self.oNavigator()
        time.sleep(2)

        self.locateInvader()


        time.sleep(0.5)
        self.cCentre()

        if not self.iP.isOnScreen(ImageRecognition.ATTACKN,5):
            return False

        self.closeWindowCheckBox(False)
        while not self.iP.isOnScreen(self.iP.CAPTURE):
            
            if (not self.cTab(self.iP.ATTACKN,1)):
                counter+= 1
            
            if counter>=10:
                self.ranOutOfEnergy()
                counter = 0
        self.cExitButton()
        self.cExitButton()

    def ranOutOfEnergy(self):
        if self.iP.isOnScreen(ImageRecognition.STORE):
            self.cTab(ImageRecognition.STORE)
            if self.iP.isOnScreen(self.iP.ENERGYBUY,4):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                time.sleep(0.3)
                if self.iP.isOnScreen(self.iP.MORE,4):
                    coords = self.iP.coordinates
                    pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                    pyautogui.click(coords)
                    time.sleep(1)
                    if self.iP.isOnScreen(self.iP.ENERGYNUMBERGOLD,5,0.7):
                        coords = self.iP.coordinates
                        pyautogui.click(coords,clicks=3,interval=0.3)
                        pyautogui.typewrite('1000')
                        time.sleep(1)
                        self.cTab(self.iP.ENERGYBUYAPPLY,5,0.8)
                        self.cExitButton()
                        return True
            self.cExitButton()


    def onMarch(self):
        return self.iP.isOnScreen(ImageRecognition.ONMARCH)

    def locateInvader(self):
        self.cTab(self.iP.XCOORD)
        self.cYesButton()

    def moveNextToInvader(self):
        pyautogui.moveTo(x=(self.width/2)-(self.width*0.07), y=(self.height/2)-(self.height*0.04),duration=self.MOUSE_SPEED)  
        pyautogui.click()
        time.sleep(0.4)
        if not self.iP.isOnScreen(self.iP.APPLY,5):
            self.cExitButton()
            pyautogui.moveTo(x=(self.width/2)+(self.width*0.07), y=(self.height/2)-(self.height*0.04),duration=self.MOUSE_SPEED)  
            pyautogui.click()
            time.sleep(0.4)
            if not self.iP.isOnScreen(self.iP.APPLY,5):
                self.cExitButton()
                pyautogui.moveTo(x=(self.width/2)+(self.width*0.07), y=(self.height/2)+(self.height*0.04),duration=self.MOUSE_SPEED)  
                pyautogui.click()
                time.sleep(0.4)
                if not self.iP.isOnScreen(self.iP.APPLY,5):
                    self.cExitButton()
                    pyautogui.moveTo(x=(self.width/2)-(self.width*0.07), y=(self.height/2)+(self.height*0.04),duration=self.MOUSE_SPEED)  
                    pyautogui.click()
                    time.sleep(0.4)
                    if not self.iP.isOnScreen(self.iP.APPLY,5):
                        self.cExitButton()
                        return False
        self.cApplyButton()
        self.cYesButton()
        return True

    def isMyTown(self):
        return self.iP.isOnScreen(ImageRecognition.TOWNISYOURS)

    def openHero(self):
        time.sleep(0.5)
        pyautogui.typewrite("h")
        time.sleep(0.5)

    def activateHeroSet(self,hSet):
        self.cTab(self.iP.HEROSETS)
        time.sleep(0.5)
        if hSet=="Invader":
            self.cTab(self.iP.INVADER)
            time.sleep(0.5)
            if self.cTab(self.iP.ACTIVATED):
                self.cTab(self.iP.EXIT)
            elif self.cTab(self.iP.ACTIVATE):
                time.sleep(0.5)
                if not self.cTab(self.iP.USE):
                    self.cTab(self.iP.BUYANDAPPLY)
            self.cTab(self.iP.EXIT)
            self.cTab(self.iP.EXIT)
            
    def cTab(self,tab,times=5,certainty=0.85):
        if self.iP.isOnScreen(tab,times,certainty):
            coords = self.iP.coordinates
            pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
            pyautogui.click()
            return True
        else:
            return False

    def cLogIn(self):
        if self.iP.isOnScreen(self.iP.LOGIN):
            coords = self.iP.coordinates
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click()

    def fullScreen(self):
        pyautogui.typewrite(['F11'])

    def cApplyButton(self):
        if self.iP.isOnScreen(self.iP.APPLY):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click(coords,clicks=2)
        return True
    
    def cYesButton(self):
        if self.iP.isOnScreen(self.iP.YES,3):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click()
        return True

    def cExitButton(self):
        if self.iP.isOnScreen(self.iP.EXIT):
            coords = self.iP.coordinates
        else:
            return False
        pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
        pyautogui.click()
        return True

    def scrollDown(self,number,intervalPeriod=0.6):
        if self.iP.isOnScreen(self.iP.SCROLLDOWN):
            coords = self.iP.coordinates
            pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
            pyautogui.click(coords,clicks=number,interval=intervalPeriod)
    
    def buyEnergy(self):
        pyautogui.typewrite('h')
        time.sleep(0.5)
        self.cTab(self.iP.ADDENERGY)
        time.sleep(0.5)
        self.scrollDown(1)
        time.sleep(0.3)
        while self.iP.isOnScreen(self.iP.APPLY,4):
            coords = self.iP.coordinates
            pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
            time.sleep(0.3)
            if self.iP.isOnScreen(self.iP.MORE,4):
                coords = self.iP.coordinates
                pyautogui.click(coords)
                if self.iP.isOnScreen(self.iP.ENERGYNUMBER,4):
                    coords = self.iP.coordinates
                    pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                    pyautogui.click(coords,clicks=3,interval=0.3)
                    pyautogui.typewrite('1000')
                    time.sleep(1)
                    self.cTab(self.iP.APPLYENERGY,5)
        if self.iP.isOnScreen(self.iP.ENERGYBUY,4):
            coords = self.iP.coordinates
            pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
            time.sleep(0.3)
            if self.iP.isOnScreen(self.iP.MORE,4):
                coords = self.iP.coordinates
                pyautogui.moveTo(coords,duration=self.MOUSE_SPEED)
                pyautogui.click(coords)
                time.sleep(1)
                if self.iP.isOnScreen(self.iP.ENERGYNUMBERGOLD,5,0.7):
                    coords = self.iP.coordinates
                    pyautogui.click(coords,clicks=3,interval=0.3)
                    pyautogui.typewrite('1000')
                    time.sleep(1)
                    self.cTab(self.iP.ENERGYBUYAPPLY,5,0.8)
                    self.cExitButton()
                    return True
                elif self.cTab(self.iP.CLOSE):
                    self.cExitButton()
                    return True
        self.cExitButton()
        return False

    def oLandmarks(self):
        self.cTab(ImageRecognition.LANDMARKS)
    
    def goToBank(self):
        self.cTab(ImageRecognition.ALL)

        time.sleep(0.8)

        self.cTab(ImageRecognition.RECIPIENT)

        time.sleep(0.8)

        self.cTab(ImageRecognition.GOTORECIPIENT)

        time.sleep(0.8)

        self.cCentre()

        time.sleep(0.8)

        if not self.cTab(ImageRecognition.HELPBTN):
            return False
        
        return True

    def dragSlider(self,slider):
        if self.iP.isOnScreen(slider):
            pyautogui.moveTo(self.iP.coordinates,duration=self.MOUSE_SPEED)
            pyautogui.mouseDown()
            pyautogui.moveRel(xOffset=int(self.width*0.3),yOffset=0)
            pyautogui.mouseUp()
            time.sleep(0.7)
            self.cTab(ImageRecognition.SEND)
        time.sleep(0.6)

    def locateSpecificInvader(self):
        invader = ImageRecognition.INVADERS.get(self.invaderType.upper(),"None")
        if invader== "None":
            print("WRONG INVADER")
            return
        while not self.iP.isOnScreen(invader):
            self.scrollDown(1)
        pyautogui.moveTo(self.iP.coordinates)
        pyautogui.moveRel(xOffset=self.width*0.4,yOffset=0)
        pyautogui.click()
        time.sleep(1)
        self.cYesButton()



    def sendResource(self,resource):
        time.sleep(1)
        if resource=="Food":
            self.dragSlider(ImageRecognition.FOODSLIDER)
        elif resource == "Lumber":
            self.dragSlider(ImageRecognition.LUMBERSLIDER)
        elif resource == "Iron":
            self.dragSlider(ImageRecognition.IRONSLIDER)
        elif resource == "Stone":
            self.dragSlider(ImageRecognition.STONESLIDER)
        elif resource == "Silver":
            self.dragSlider(ImageRecognition.SILVERSLIDER)


