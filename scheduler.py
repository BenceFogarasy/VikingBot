from apscheduler.schedulers.background import BackgroundScheduler

class Repeat:
    def __init__(self,toDo,repeatTime):
        self.isQuit = False
        self.scheduler = BackgroundScheduler()
        self.job = None
        self.i = 1
        self.addJob(toDo,repeatTime)

    def addJob(self,toDo,repeatTime=1800):
        print("Job added every "+str(repeatTime))
        self.job = self.scheduler.add_job(toDo, 'interval', seconds=repeatTime,max_instances=3)

    def startJobs(self):
        print("Started job")
        self.scheduler.start()

    def quitJob(self):
        self.scheduler.remove_all_jobs()
        self.scheduler.shutdown(wait=False)
    
    def sayHi(self):
        print("Hi")
        self.i += 1
        if self.i==3:
            self.pauseJob()
            self.resumeJob()
            

    def resumeJob(self):
        self.scheduler.resume()

    def pauseJob(self):
        self.scheduler.pause()
        print("paused")


#   ------------------        usage:          ----------------------
# s = Repeat()

# try:
#    s.startJobs() 
# except (KeyboardInterrupt, SystemExit):
#    s.quitJob()