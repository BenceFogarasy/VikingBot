import cv2 as cv
import numpy as np
import time
import pyautogui
from pathlib import Path

class ImageRecognition:
    DIRECTORY =  str(Path(__file__).parent.absolute())+r"\pics"
    EXIT =     DIRECTORY+r"\exit.png"
    APPLY =    DIRECTORY+r"\apply.png"
    CHEST =    DIRECTORY+r"\chest.png"
    EMAIL =    DIRECTORY+r"\email.png"
    HELP =     DIRECTORY+r"\help.png"
    ICON =     DIRECTORY+r"\icon.png"
    LOGIN =    DIRECTORY+r"\logIn.png"
    LOGOUT =   DIRECTORY+r"\logOut.png"
    RETURNED = DIRECTORY+r"\returned.png"
    PASSWORD = DIRECTORY+r"\password.png"
    PLAYNOW =  DIRECTORY+r"\playNow.png"
    RESTART =  DIRECTORY+r"\restart.png"
    SELECTLOCATIONTYPE =DIRECTORY+r"\selectLocationType.png"
    TASKMENU = DIRECTORY+r"\taskMenu.png"
    USERICON = DIRECTORY+r"\userIcon.png"
    YES =      DIRECTORY+r"\yesBtn.png"
    XINPUT =   DIRECTORY+r"\xInput.png"
    YINPUT =   DIRECTORY+r"\yInput.png"
    GOTO =             DIRECTORY+r"\goTo.png"
    USERLOGIN =DIRECTORY+r"\userLogIn.png"
    LOGOUTYES =DIRECTORY+r"\logOutYes.png"
    INVADER =  DIRECTORY+r"\invader.png"
    LOCATIONTYPEINVADER =  DIRECTORY+r"\locationTypeInvader.png"
    SECONDMENU =  DIRECTORY+r"\secondMenu.png"
    SECONDMENU2 =  DIRECTORY+r"\secondMenu2.png"
    XCOORD =  DIRECTORY+r"\xCoord.png"
    SCROLLDOWN =  DIRECTORY+r"\scrollDown.png"
    LEVEL1 =   DIRECTORY+r"\level1.png"
    LEVEL6 =   DIRECTORY+r"\level6.png"
    INVADEROPTION =   DIRECTORY+r"\invaderOption.png"
    UBER =     DIRECTORY+ r"\uber.png"
    INFO =     DIRECTORY+r"\info.png"
    ATTACKE =  DIRECTORY+r"\attackE.png"
    ATTACKN =  DIRECTORY+r"\attackN.png"
    ACTIVATE =  DIRECTORY+r"\activate.png"
    ACTIVATED =  DIRECTORY+r"\activated.png"
    HEROSETS =  DIRECTORY+r"\heroSetS.png"
    USE =      DIRECTORY+ r"\use.png"
    CLOSE =      DIRECTORY+r"\close.png"
    BUYANDAPPLY =  DIRECTORY+r"\buyAndApply.png"
    CHECKBOX = DIRECTORY+r"\checkBox.png"
    CHECKEDBOX = DIRECTORY+r"\checkedBox.png"
    CLOSEWINDOW =      DIRECTORY+r"\closeWindow.png"
    WINDOWCLOSED =      DIRECTORY+r"\windowClosed.png"
    RECALL =   DIRECTORY+r"\recall.png"
    CAPTURE =   DIRECTORY+r"\capture.png"
    ADDENERGY =   DIRECTORY+r"\addEnergy.png"
    ENERGYNUMBER =   DIRECTORY+r"\energyNumber.png"
    ENERGYNUMBERGOLD =   DIRECTORY+r"\energyNumberGold.png"
    ENERGYBUY =   DIRECTORY+r"\energyBuy.png"
    ENERGYBUYAPPLY =   DIRECTORY+r"\energyBuyApply.png"
    APPLYENERGY =   DIRECTORY+r"\applyEnergy.png"
    MORE =   DIRECTORY+r"\more.png"
    RESOURCEICONS =   DIRECTORY+r"\resourceIcons.png"
    VIKINGLOGO =   DIRECTORY+r"\vikingLogo.png"
    VIKINGMENU =   DIRECTORY+r"\vikingMenu.png"
    FIRSTINFO =   DIRECTORY+r"\firstInfo.png"
    CLANTASK =   DIRECTORY+r"\clanTask.png"
    PREMIUMTASK =   DIRECTORY+r"\premiumTask.png"
    CLAIMALL =   DIRECTORY+r"\claimAll.png"
    CLAIM =   DIRECTORY+r"\claim.png"
    STORE =   DIRECTORY+r"\store.png"
    GEM =   DIRECTORY+r"\gem.png"
    FUSE =   DIRECTORY+r"\fuse.png"
    FUSE2 =   DIRECTORY+r"\fuse2.png"
    BOOST =   DIRECTORY+r"\boost.png"
    APPLY3H =   DIRECTORY+r"\apply3h.png"
    FREE =   DIRECTORY+r"\free.png"
    ONMARCH =   DIRECTORY+r"\onMarch.png"
    NAVIGATOR =   DIRECTORY+r"\navigator.png"
    TOWNISYOURS =   DIRECTORY+r"\townIsYours.png"
    TASKCOMPLETED =   DIRECTORY+r"\taskCompleted.png"
    START =   DIRECTORY+r"\start.png"
    INVADERS = {
        "GASCON" :  DIRECTORY+r"\gascon.png",
        "SERPENT" :   DIRECTORY+r"\serpent.png",
        "ROYALGUARDSMAN" :   DIRECTORY+r"\royalGuardsman.png",
        "CELT" :   DIRECTORY+r"\celt.png",
        "SARACEN" :   DIRECTORY+r"\saracen.png",
        "CANIS" :   DIRECTORY+r"\canis.png",
        "LONGOBARD" :   DIRECTORY+r"\longobard.png"
    }
    RIGHTUPPER =   DIRECTORY+r"\rightUpper.png"
    LEFTLOWER =   DIRECTORY+r"\rightLower.png"
    LANDMARKS =   DIRECTORY+r"\landMarks.png"
    ALL =   DIRECTORY+r"\all.png"
    RECIPIENT =   DIRECTORY+r"\recipient.png"
    GOTORECIPIENT =   DIRECTORY+r"\goToRecipient.png"
    HELPBTN =   DIRECTORY+r"\helpBtn.png"
    FOODSLIDER =   DIRECTORY+r"\foodSlider.png"
    LUMBERSLIDER =   DIRECTORY+r"\lumberSlider.png"
    IRONSLIDER =   DIRECTORY+r"\ironSlider.png"
    STONESLIDER =   DIRECTORY+r"\stoneSlider.png"
    SILVERSLIDER =   DIRECTORY+r"\silverSlider.png"
    SEND =   DIRECTORY+r"\send.png"



    def __init(self):
        self.coordinates = []
    
    def isOnScreen(self,needle,tries=2,delay=0,thresh=0.85):
        while tries>0:
            ps = pyautogui.screenshot()

            haystack_img =  cv.cvtColor(np.array(ps), cv.COLOR_RGB2BGR)
            needle_img = cv.imread(needle,cv.IMREAD_COLOR)

            result = cv.matchTemplate(haystack_img,needle_img,cv.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            threshold = thresh
            
            if max_val >= threshold:
                x = int(max_loc[0]+needle_img.shape[1]/2)
                y = int(max_loc[1]+needle_img.shape[0]/2)
                self.coordinates = [x,y]
                print("Found: "+needle)
                return True
                break
            tries -= 1
            if delay!=0:
                time.sleep(delay)
            print("Not found:"+ needle)
        return False

    def getObjectsOnScreen(self,needle,tries=2,delay=0,thresh=0.85):
        while tries>0:
            ps = pyautogui.screenshot()

            haystack_img =  cv.cvtColor(np.array(ps), cv.COLOR_RGB2BGR)
            needle_img = cv.imread(needle,cv.IMREAD_COLOR)

            result = cv.matchTemplate(haystack_img,needle_img,cv.TM_CCOEFF_NORMED)

            threshold = thresh
            
            locations = np.where(result >= threshold)

            locations = list(zip(*locations[::-1]))
            coordinateList = []
            for i in locations:
                x = int(i[0]+needle_img.shape[1]/2)
                y = int(i[1]+needle_img.shape[0]/2)

                coordinateList.append([x,y])
            if len(coordinateList) >=1:
                print("Found: "+needle+" "+str(len(coordinateList))+" times.")
                return coordinateList
                break
            
            tries -= 1
            if delay!=0:
                time.sleep(delay)
            print("Not found:"+ needle)
        return False

    def getHeight(self):
        return len(np.array(pyautogui.screenshot()))

    def getWidth(self):
        return len(np.array(pyautogui.screenshot())[0])

    def isShielded(self):
        ps = pyautogui.screenshot()
        img =  cv.cvtColor(np.array(ps), cv.COLOR_RGB2HSV)

        h= int(len(img))
        w = int(len(img[0]))
        img = img[ int(h/2- 50):int(h/2+70),int(w/2-85):int(w/2+80)]
        


        lower = np.array([103,140,170])
        upper = np.array([122,255,255])

        result = img.copy()
        mask =cv.inRange(result,lower,upper)
        result = cv.bitwise_and(result, result, mask=mask)
        result =  cv.cvtColor(result, cv.COLOR_HSV2BGR)

        threshold = 205000
        certainty = np.sum(result) / threshold 
        
        if certainty >= 0.95:
            return True
        else:
            return False

    def processNumber(self):
        ps = pyautogui.screenshot()

        img =  cv.cvtColor(np.array(ps), cv.COLOR_RGB2BGR)
        needleLeftLower = cv.imread(self.LEFTLOWER,cv.IMREAD_COLOR)
        needleRightUpper = cv.imread(self.RIGHTUPPER,cv.IMREAD_COLOR)

        rightUpper = cv.matchTemplate(img,needleRightUpper,cv.TM_CCOEFF_NORMED)

        leftLower = cv.matchTemplate(img,needleLeftLower,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, leftLowerCorner = cv.minMaxLoc(leftLower)
        min_val2, max_val2, min_loc2, rightUpperCorner = cv.minMaxLoc(rightUpper)

        hLL= int(len(needleLeftLower))
        wLL = int(len(needleLeftLower[0]))
        hRU= int(len(needleRightUpper))
        wRU = int(len(needleRightUpper[0]))

        
        # cv.circle(img, (leftLowerCorner[0]+hLL,rightUpperCorner[1]), 3, (255, 0, 255) , thickness=4, lineType=8, shift=0)
        # cv.circle(img, (rightUpperCorner[0],rightUpperCorner[1]+hRU), 3, (0, 0, 255) , thickness=4, lineType=8, shift=0)
        # cv.imshow("Frame",img)

        crop_img = img[
            rightUpperCorner[1]    :        rightUpperCorner[1]+hRU     
            ,         
           leftLowerCorner[0]+hLL     :        rightUpperCorner[0]
                         
                         ]
        
        cv.imshow("Frame2",crop_img)

        cv.waitKey()

