import sys
import myUI as uI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QTreeWidgetItem,QTreeWidget,QFileDialog 
import os
import time
import automate
from menu import Menu
import threading
from pathlib import Path
import scheduler
class Application:
    PROGRESSBAR_SPEED = 0.03
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = uI.Ui_MainWindow()
        self.directory =  str(Path(__file__).parent.absolute())+"\pics"
        self.database =  str(Path(__file__).parent.absolute())+r"\database"
        self.ui.setupUi(self.MainWindow,self.directory)
        self.MainWindow.show()
        self.automation = None
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        id =self.getCurrentId()
        self.Info = Info(id)
        self.ChosenProfile = Info()
        self.storedProgress = 0
        self.isBrowserLoaded = False

        self.enterProfile()
        self.initialiseListeners()
        self.populateDynamicElements()
        sys.exit(self.app.exec_())

    def initialiseListeners(self):
        self.ui.btnJob.clicked.connect(self.enterJob)
        self.ui.btnProfile.clicked.connect(self.enterProfile)
        self.ui.btnMain.clicked.connect(self.enterMain)
        self.ui.btnBrowser.clicked.connect(self.enterBrowser)
        self.ui.btnHelp.clicked.connect(self.showHelp)
        self.ui.btnAddProf.clicked.connect(self.addProfile)
        self.ui.btnDelete.clicked.connect(self.removeProfile)
        self.ui.btnSelectProf.clicked.connect(self.selectProfile)
        self.ui.rbInvader.clicked.connect(lambda: self.chooseJob("Invader Hunt"))
        self.ui.rbResources.clicked.connect(lambda: self.chooseJob("Transfer Resources"))
        self.ui.rbTasks.clicked.connect(lambda: self.chooseJob("Task Completion"))
        self.ui.rbYielding.clicked.connect(lambda: self.chooseJob("Yielding"))
        self.ui.btnChooseBrowser.clicked.connect(self.chooseBrowser)
        self.ui.btnStart.clicked.connect(self.startBot)
        self.ui.cbResourceProfile.currentIndexChanged.connect(self.changeTypeToGroup)

    def enterBrowser(self):
        self.ui.btnProfile.setFlat(False)
        self.ui.btnJob.setFlat(False)
        self.ui.btnMain.setFlat(False)
        self.ui.btnBrowser.setFlat(True)
        self.ui.gbJob.hide()
        self.ui.gbBrowser.show()
        self.ui.gbMain.hide()
        self.ui.gbProfile.hide()
        if self.isBrowserLoaded:
            self.increaseStatusBar(75)
    
    def enterProfile(self):
        self.ui.btnProfile.setFlat(True)
        self.ui.btnJob.setFlat(False)
        self.ui.btnMain.setFlat(False)
        self.ui.btnBrowser.setFlat(False)
        self.ui.gbJob.hide()
        self.ui.gbBrowser.hide()
        self.ui.gbMain.hide()
        self.ui.gbProfile.show()

    def enterJob(self):
        self.ui.btnProfile.setFlat(False)
        self.ui.btnJob.setFlat(True)
        self.ui.btnMain.setFlat(False)
        self.ui.btnBrowser.setFlat(False)
        self.ui.gbJob.show()
        self.ui.gbBrowser.hide()
        self.ui.gbMain.hide()
        self.ui.gbProfile.hide()

    def enterMain(self):
        self.ui.btnProfile.setFlat(False)
        self.ui.btnJob.setFlat(False)
        self.ui.btnMain.setFlat(True)
        self.ui.btnBrowser.setFlat(False)
        self.ui.gbJob.hide()
        self.ui.gbBrowser.hide()
        self.ui.gbMain.show()
        self.ui.gbProfile.hide()
        self.fillProfileInfo()
        self.increaseStatusBar(100)
        self.checkIsRead()

    def fillProfileInfo(self):
        self.getJobDetails()
        browser = self.ChosenProfile.browser.split('/')
        content = "PROFILE INFORMATION\n"
        content += "ID: "+str(self.ChosenProfile.id) + "\n"
        content += "Email: "+str(self.ChosenProfile.email) + "\n"
        content += "Pw: "+str(self.ChosenProfile.password) + "\n"
        content += "Group: "+str(self.ChosenProfile.group) + "\n"
        content += "Browser: "+str(browser[len(browser)-1]) + "\n"
        content += "\nJob: "+str(self.ChosenProfile.job) + "\n"
        content += "Details: \n"
        for i in self.ChosenProfile.details:
            content += "-"+str(i) + "\n"

        self.ui.label_20.setText(content)
        self.ui.label_20.adjustSize()
        self.ui.label_20.adjustSize()
        self.ui.label_20.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)

    def getJobDetails(self):
        tempDetails = []
        if self.ChosenProfile.job=="":
            return
        if self.ChosenProfile.job == "Invader Hunt":
            invaderLevel = self.ui.cbInvaderLevel.currentText()
            invaderType = self.ui.cbInvaderType.currentText()
            tempDetails.append("Invaderlevel:"+invaderLevel)
            tempDetails.append("InvaderType:"+invaderType)
        elif self.ChosenProfile.job == "Yielding":
            yieldingLevel = self.ui.cbYieldingLevel.currentText()
            yieldingType = self.ui.cbYieldingType.currentText()
            tempDetails.append("YieldingLevel:"+yieldingLevel)
            tempDetails.append("YieldingType:"+yieldingType)
        elif self.ChosenProfile.job == "Task Completion":
            taskLevel = self.ui.cbTasks.currentText()
            tempDetails.append("TaskLevel:"+taskLevel)
        elif self.ChosenProfile.job == "Transfer Resources":
            resourceTime = self.ui.cbResourceTime.currentText()
            resourceType = self.ui.cbResourceType.currentText()
            resourceProfile = self.ui.cbResourceProfile.currentText()
            tempDetails.append("ResourceTime:"+resourceTime)
            tempDetails.append("ResourceType:"+resourceType)
            tempDetails.append("ResourceProfile:"+resourceProfile)
        else:
            self.showError("INVALID JOB DETAILS")
            return
        self.ChosenProfile.details = tempDetails

    def checkIsRead(self):
        if (self.ChosenProfile.id != 0 and self.ChosenProfile.email != "" and self.ChosenProfile.group!=""  and
            self.ChosenProfile.password!="" and self.ChosenProfile.job!=""
             and self.ChosenProfile.browser!="" and len(self.ChosenProfile.details)!=0):
            self.ui.btnStart.setEnabled(True)

    def getCurrentId(self):
        content = self.readFile(self.database+"\profiles.txt")
        biggest = 0
        if content==False:
            return 0
        else:
            for i in content:
                idCurrent = i.split(',')[0]
                if int(idCurrent) > biggest:
                    biggest = int(idCurrent)
        return biggest

    def changeTypeToGroup(self):
        self.ui.cbResourceType.setCurrentIndex(self.ui.cbResourceProfile.currentIndex())

    def groupAccounts(self,group):
        content = self.readFile(self.database+"\profiles.txt")
        profiles = []
        if content==False:
            self.showError("Missing file")
            return False
        else:
            for i in content:
                currentGroup = i.split(',')[3]
                if currentGroup.strip().lower() == group.strip().lower():
                    profiles.append(i)
        
        return self.processProfiles(profiles)

    def processProfiles(self,inProfiles):
        outProfiles = []
        for i in inProfiles:
            i  =  i[:-3]
            tempProf = i.split(',')
            dummy = Info(tempProf[0],tempProf[1],tempProf[2],tempProf[3])
            outProfiles.append(dummy)
        return outProfiles


    def getSelectedGroup(self):
        prof= self.ui.cbResourceProfile.currentText()
        prof =  str(prof.split(' ')[0])
        if prof=="Just":
            return "None"
        else:
            return prof

    def startBot(self):
        profiles = None
        if self.ChosenProfile.job=="Transfer Resources":
            if self.getSelectedGroup()=="None":
                profiles = []
            else:
                profiles = self.groupAccounts(self.getSelectedGroup())
        self.MainWindow.close()
        self.automation = automate.Automate(self.ChosenProfile,profiles)
        self.menu = automate.openWindow(self.automation)
        self.automation.setMenu(self.menu)
        self.threadpool.start(self.automation)
        print(QtCore.QThreadPool().activeThreadCount())


    def chooseBrowser(self):
        filename = QFileDialog.getOpenFileName(None,
            ("Select Browser"), "c://", ("Executables (*.exe )"))
        filename = filename[0]
        if(filename=="" or filename==" " or filename == None):
            self.showError("Please select a valid browser!")
            return
        self.writeFile(self.database+r"\browser.txt",filename)
        self.ui.lblBrowser.setText(str(filename))
        self.ui.lblBrowser.adjustSize()
        self.increaseStatusBar(75)
        self.loadInBrowser()


    def addProfile(self):
        email = self.ui.leEmail.text()
        password = self.ui.lePassword.text()
        group = self.ui.cbProfGroup.currentText()
        if(email=="" or password == ""):
            self.showError("EMAIL OR PASSWORD MISSING")
            return
        self.Info.email = email
        self.Info.password = password
        self.Info.group = group
        self.Info.id += 1
        self.displayProfile(self.Info)
        self.saveProfile(self.Info)

    def saveProfile(self,obj):
        with open(self.database+r"\profiles.txt",'a') as f:
            f.writelines(str(obj.id)+","+obj.email+","+obj.password+","+obj.group+"\n")

    def displayProfile(self,obj):
        profile =  QTreeWidgetItem(self.ui.treeProfiles)
        profile.setText(0,str(obj.id))
        profile.setText(1,obj.email)
        profile.setText(2,obj.password)
        profile.setText(3,obj.group)

    def populateDynamicElements(self):
        self.loadInBrowser()
        profiles = self.readFile(self.database+"\profiles.txt")
        if profiles!=False:
            for i in profiles:
                t = i.split(',')
                dummy = Info(t[0],t[1],t[2],t[3])
                self.displayProfile(dummy)
        else:
            print("Document not found")
        self.clearUpTree()
    
    def loadInBrowser(self):
        content = self.readFile(self.database+r"\browser.txt") 
        if content!=False:
            self.ui.lblBrowser.setText(content[0])
            self.ChosenProfile.browser = content[0]
            self.isBrowserLoaded = True

    def chooseJob(self,jobType):
        self.ChosenProfile.job = jobType
        self.increaseStatusBar(75)

    def clearUpTree(self):
        empty = (self.ui.treeProfiles.findItems("", QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive))
        self.ui.treeProfiles.itemAt(0, 0).setHidden(True)
        for i in range(len(empty)):
            empty[i].setHidden(True)
            self.ui.treeProfiles.removeItemWidget(empty[i],0)

    def removeProfile(self):
        selected = self.ui.treeProfiles.selectedItems()
        for i in selected:
            i.setHidden(True)
            bad_words = [str(i.text(0))]
            with open(self.database+'\profiles.txt','r') as oldfile, open(self.database+'\profilesT.txt', 'w') as newfile:
                for line in oldfile:
                    if not any(bad_word in line for bad_word in bad_words):
                        newfile.write(line)
            os.remove(self.database+"\profiles.txt")     
            os.rename(self.database+'\profilesT.txt', self.database+'\profiles.txt')

    def selectProfile(self):
        if len(self.ui.treeProfiles.selectedItems())==0:
            self.showError("Please select a valid profile!")
            return
        selected = self.ui.treeProfiles.selectedItems()[0]
        for i in range(4):
            if selected.text(i)=="":
                self.showError("Please select a valid profile!")
                return
        self.ChosenProfile.id = int(selected.text(0))
        self.ChosenProfile.email =  selected.text(1)
        self.ChosenProfile.password = selected.text(2)
        self.ChosenProfile.group =  selected.text(3)
        self.increaseStatusBar(75)

    def increaseStatusBar(self,value):
        if value==100 and self.storedProgress!=75:
            return
        if value>25 and self.storedProgress==0:
            value = 25
        if value>50 and self.storedProgress==25:
            value = 50
        for i in range(self.storedProgress,value):
            time.sleep(self.PROGRESSBAR_SPEED)
            self.ui.progressBar.setValue(i+1)
        if self.storedProgress<value:
            self.storedProgress = value

    def readFile(self,fileName):
        if os.path.isfile(fileName):
            with open(fileName,'r') as f:
                temp = f.readlines()
                return temp
        else:
            return False

    def writeFile(self,fileName,content):
        with open(fileName,'w') as f:
            f.write(content)
    def showError(self,error):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(error)

        x= msg.exec_()

    def showHelp(self):
        msg = QMessageBox()
        msg.setWindowTitle("Help")
        msg.setText("HEllo")

        x= msg.exec_()
       


class Info:
    def __init__(self,id=0,em="",pw="",gr=""):
        self.email = em
        self.password = pw
        self.url  = 'https://plarium.com/en/strategy-games/vikings-war-of-clans/game/\n'
        self.browser = ""
        self.profiles = []
        self.job = ""
        self.id = id
        self.details = []
        self.group = gr

    def printDetails(self):
        print(
            self.email + "  "+
            self.password 
        )
        

if __name__ == "__main__":
    app = Application()