import os
import guiControl 
import time
import relocation
from menu import Menu
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback, sys
from pathlib import Path
import scheduler
class Automate(QRunnable):

    COOLDOWN_PERIOD = 0.5
    WAIT_PERIOD = 1.5
    LONG_WAIT = 5
    RADIUS = 50
    TRANSFERS = 10
    STARTINGCOORDINATE = 0
    def __init__(self,obj,profiles=None,):
        super(Automate,self).__init__()
        self.Inst = obj
        self.directory =   str(Path(__file__).parent.absolute())+"\pics"#r"D:\Projects\bot\timing_bot\pics"
        self.profiles = profiles
        self.gC = guiControl.guiControl(0.5)
        self.setAutoDelete(True)
        self.signals = WorkerSignals()  
        
        self.taskType = None
        self.taskChanged = False
        self.hasClosed = False

        self.R = None
        self.currentCoordinate = 0
        self.coordinateLength = 0

        self.currentProfile = 0
        self.firstTransfer = True

    @pyqtSlot()
    def run(self):
        self.Start()

    def setMenu(self,obj):
        self.menu = obj

    def invaderCounter(self):
        self.menu.updateInvaderCount(self.gC.invadersSlain)

    def Start(self):
        self.work()
        # self.finishWork()
    
    def checkStopped(self):
        if self.hasMenuClosed():
            self.finishWork()
            sys.exit()
            return

    def enterGame(self):
        self.coolDown(self.WAIT_PERIOD)
        self.gC.goToWebsite(self.Inst.browser,str(self.Inst.url))
        if self.hasMenuClosed():
            return False
        self.checkStopped()
        self.coolDown(self.WAIT_PERIOD)
        self.gC.fullScreen()
        self.coolDown(self.WAIT_PERIOD)
        
        self.logIn()
        self.loadGame()
        if self.hasMenuClosed():
            return False
        self.checkStopped()
        
        # self.finishWork()
        self.gC.closePopUps(3)

        self.coolDown(2)
        return True

    def finishWork(self):
        print(QtCore.QThreadPool().activeThreadCount())
        self.signals.finished.emit() 
        self.menu.close()
        self.gC.quitWindow()
        sys.exit()

    def loadGame(self):
        while not self.gC.isLoaded() and not self.hasMenuClosed():
           time.sleep(1)
       
    def hasMenuClosed(self):
        if self.hasClosed == True:
            self.gC.hasClosed = True
            return True
        else:
            return False

    def work(self):
        if self.Inst.job == "Invader Hunt":
            invaderType = self.Inst.details[1].split(':')[1]
            print(invaderType)
            if invaderType!="Any":
                self.gC.invaderType = invaderType
            if not self.enterGame():
                return False
            self.R = relocation.Relocation(50,1)
            self.activateInvaderSet()
            self.gC.oMap()
            if(self.Inst.details[0]=="Invaderlevel:Level 1"):
                print("Level 1")
                self.huntInvader(1)
            elif(self.Inst.details[0]=="Invaderlevel:Level 6"):
                print("Level 6")
                self.huntInvader(6)
            else:
                print("Uber")
                self.huntInvader(7)
                
        elif self.Inst.job == "Yielding":
            if not self.enterGame():
                return False
        elif self.Inst.job == "Task Completion":
            if not self.enterGame():
                return False
            self.completeTasks()
        elif self.Inst.job == "Transfer Resources":
            
            if len(self.profiles)==0:
                print(self.Inst.printDetails())
                self.activateTransfer()
            else:
                for i in range(len(self.profiles)):
                    self.switchAccount(i)
                    if not self.activateTransfer():
                        return False
                        break


            if self.firstTransfer:
                self.scheduler = scheduler.Repeat(self.work,self.getTransferTime())
                self.scheduler.startJobs()
                self.firstTransfer = False
            
                      
        else:
            print("shit")
    
    def activateTransfer(self):
        if not self.enterGame():
            return False
        self.transferResources()  
        return True

    def switchAccount(self,current):
        self.Inst.email = self.profiles[current].email
        self.Inst.password = self.profiles[current].password

    def activateInvaderSet(self):
        self.gC.openHero()
        self.gC.activateHeroSet("Invader")

    def completeTasks(self):
        print("COMPLETING TASKS")
        self.taskType = str(self.Inst.details[0]).split(':')[1] 
        self.gC.taskManager()
        while True and not self.hasClosed:
            if not self.gC.completeTask(self.taskType):
                break
            self.coolDown(0.3)
        return
        
    def changeTaskType(self,newType):
        self.taskChanged = True
        self.taskType = newType

    def getTransferTime(self):
        resourceTime = str(self.Inst.details[0]).split(':')[1] 
        if resourceTime == "40mins":
            resourceTime = int(40*60)
        elif resourceTime=="1hour":
            resourceTime = int(1*60)
        elif resourceTime == "2hours":
            resourceTime = int(2*60)
        return resourceTime
        

    def transferResources(self):
        print("Sending resources")
        resourceType = str(self.Inst.details[1]).split(':')[1] 
        resourceTime = str(self.Inst.details[0]).split(':')[1] 
        resourceGroup = str(self.Inst.details[2]).split(':')[1] 

        self.coolDown()

        self.gC.oMap()
        self.coolDown()

        self.gC.oLandmarks()
        self.coolDown()

        if not self.gC.goToBank():
            self.finishWork()
            return False
        self.coolDown()
        for i in range(self.TRANSFERS):
            self.gC.sendResource(resourceType)
            self.coolDown()
            if resourceType!="Silver":
                self.gC.sendResource("Silver")
                self.coolDown()

        
        self.gC.cExitButton()
        self.coolDown()
        self.gC.cExitButton()
        self.coolDown()
        self.gC.quitWindow()

    def huntInvader(self,level):
        self.R = relocation.Relocation(self.RADIUS,int(level))
        if level==1:
            self.gC.oNavigator()
            self.gC.selectLocationType(level)
            self.coolDown(2)
            while True and not self.hasMenuClosed():
                self.gC.buyEnergy()
                self.coolDown(2)
                self.moveToNextCoordinate()
                self.killInvaders(level)
        elif level==6:
            self.R.relocateTown(self.R.x[0],self.R.y[0])
            self.gC.oNavigator()
            self.gC.selectLocationType(level)
            self.coolDown(2)
            self.killInvaders(6)
        else:
            self.R.relocateTown(self.R.x[0],self.R.y[0])
            self.gC.oNavigator()
            self.gC.selectLocationType(level)
            self.coolDown(2)
            self.killInvaders(7)
 
    def moveToNextCoordinate(self):
        
        self.coordinateLength = len(self.R.x)

        if (self.currentCoordinate == 0):
            self.currentCoordinate = self.STARTINGCOORDINATE

        self.R.current = self.currentCoordinate
        self.R.relocateTown(self.R.x[self.currentCoordinate],self.R.y[self.currentCoordinate])

        if self.currentCoordinate == self.coordinateLength:
            self.currentCoordinate = self.STARTINGCOORDINATE
        else:
            self.currentCoordinate += 1

        
        self.coolDown(2)
        self.gC.oNavigator()




    def killInvaders(self,level):
        if level==1:
            while self.gC.killLevel1Invader()!=False and not self.hasMenuClosed():
                self.invaderCounter()
                pass
            time.sleep(1.5)
            self.gC.cExitButton()
            while self.gC.onMarch() and not self.hasMenuClosed():
                time.sleep(1)
        else:
            while True and not self.hasMenuClosed():
                self.invaderCounter()
                self.gC.killInvaders()


    def logIn(self):
        if(self.gC.isLoggedIn()):
            self.gC.logOut()
            time.sleep(self.LONG_WAIT)
        self.gC.logIn(self.Inst.email,self.Inst.password)
        self.gC.cPlayNow()
        self.coolDown(10)


    def coolDown(self,period=0):
        if period!=0:
            time.sleep(period)
            return
        time.sleep(self.COOLDOWN_PERIOD)


class openWindow:
    def __init__(self,automateClass):
        super().__init__()
        self.height = guiControl.guiControl(1).getHeight()
        self.width = guiControl.guiControl(1).getWidth()
        self.directory =  str(Path(__file__).parent.absolute())+"\pics"#r"D:\Projects\bot\timing_bot\pics"
        self.signals = WorkerSignals()
        self.automate = automateClass
        self.show()


    def quitFn(self):
        self.automate.hasClosed = True
        self.signals.finished.emit() 

    def show(self):
        self.myMenu = Menu(self.directory,self.quitFn)
        self.myMenu.show()
        self.myMenu.setButtonAction(self.automate)
        self.myMenu.setGeometry(QtCore.QRect(int(self.width*0.8),int(self.height*0.78), 270, 150))
    
    def close(self):
        self.myMenu.close()

    def updateInvaderCount(self,number):
        self.myMenu.updateInvaderCount(number)
        



class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)