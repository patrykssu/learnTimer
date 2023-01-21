import plyer
import time
import threading
import json


dates = {}
start_time = ""

settings = {}


class Learner():
    settings = {}
    info = {}


    # learn Area
    def startLearn(self):
        print("----------------------------------------------")
        print("NOTICE: you can stop learning every time you want")
        print("just by write exit or 0 or return")
        print("----------------------------------------------")

        self.info['totalSessions'] += 1
        self.info['totalLearns'] += 1
        self.info['lastLearnTime'] = time.ctime(time.time())
        self.islearning = True

        plyer.notification.notify(
            title="Learning Started",
            app_icon='learn.ico',

            message="Enjoy your Study time! Break in " +
                    str(self.settings['learnTime']) + " minutes!",

            timeout=80
        )

        temp = threading.Thread(target=self.timeLearning, daemon=True)
        temp.start()

        while True:
            answer = input(">>>>")
            answer = answer.lower()
            if answer in ("0", "exit", "return", "quit"): break

        self.islearning = False


    def timeLearning(self):
        type = 'learn'
        temp_time = 0
        while True:
            if not self.islearning: break

            time.sleep(1)
            temp_time += 1


            if type == 'learn':
                self.info['totalLearnTime'] += 1
                if temp_time >= self.settings['learnTime'] * 60:
                    temp_time = 0
                    type = 'break'
                    self.info['totalBreaks'] += 1
                    plyer.notification.notify(
                        title = "BREAK!",
                        app_icon = 'break.ico',

                        message = "I guess that you currently have to make break for at least " +
                                  str( self.settings['breakTime']) + " minutes!",

                        timeout = 140
                    )

            else:
                self.info['totalBreakTime'] += 1
                if temp_time >= self.settings['breakTime'] * 60:
                    temp_time = 0
                    type = 'learn'
                    self.info['totalLearns'] += 1
                    plyer.notification.notify(
                        title = "LEARN!",
                        app_icon = 'learn.ico',

                        message = "Your break time is over, you have to study for at least " +
                                  str( self.settings['learnTime']) + " minutes!",

                        timeout = 140
                    )



    # settings Area
    def loadSettings(self):
        try:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)

        except:
            self.newSettings()

    def saveSettings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def newSettings(self):
        self.settings = \
            {
                "_comment":"BETTER change it by program",
                "breakTime":5,
                "learnTime":30,
            }
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def changeSettings(self):
        while True:
            print("----------------------------------------------")
            print("1/break -> change your break time ("  + str(self.settings['breakTime']) + "m) ")
            print("2/work/learn -> change your learn time ("  + str(self.settings['learnTime']) + "m) ")
            print("0/return -> RETURN")
            print("----------------------------------------------")
            answer = input(">>>>")
            if not answer.isnumeric():
                answer = answer.lower()
            match answer:
                case "1" | "break" | "free" | "breaktime" | "freetime":
                    newtime = int(input("new break time: "))
                    self.settings['breakTime'] = newtime
                case "2" | "work" | "worktime" | "learn" | "learntime":
                    newtime = int(input("new learn time: "))
                    self.settings['learnTime'] = newtime
                case "0" | "quit" | "exit" | "return": break

                case _: pass

    # statistic Area
    def saveStatiscs(self):
        with open("statistics.json", "w") as file:
            json.dump(self.info, file, indent=4)
    def loadStastics(self):
        try:
            with open("statistics.json", "r") as file:
                self.info = json.load(file)
        except:
            self.newStatistic()
    def newStatistic(self):
        self.info = {
            "_comment": "Be sure what are you doing here",
            "lastLearnTime": 'none',
            "totalLearnTime": 0,
            "totalBreakTime": 0,
            "totalSessions": 0,
            "totalBreaks": 0,
            "totalLearns": 0

        }
        with open("statistics.json", "w") as file:
            json.dump(self.info, file, indent=4)

    def showStatistics(self):
        while True:
            print("----------------------------------------------")
            print("Break time: {}m      Learn time: {}m".format(str(self.info['totalBreakTime']), str(self.info['totalLearnTime'])))
            print("Total Breaks: {}      Total Learns: {}".format(str(self.info['totalBreaks']), str(self.info['totalLearns'])))
            print("Last session: {} (SESSION NR: {} )".format(str(self.info['lastLearnTime']), str(self.info['totalSessions'])))
            print("----------------------------------------------")
            print("0/RETURN -> Return  |   1 / RESTART -> RESTART STATISTICS")
            answer = input(">>>>")
            if not answer.isnumeric():
                answer = answer.lower()
            match answer:
                case "1" | "restart" | "new":
                    while True:
                        print("Are you sure? (Y/N)")
                        answer = input(">>>>")
                        answer = answer.lower()
                        if answer == "y":
                            self.newStatistic()
                            break
                        elif answer == "n":
                            break
                case "0" | "quit" | "exit" | "return":
                    break

                case _:
                    pass


    # menu Area
    def menu(self):
        self.loadSettings()
        self.loadStastics()
        while True:
            print("----------------------------------------------")
            print("1/start     -> Start Learning")
            print("2/information   -> Informations and credits")
            print("3/settings  -> settings")
            print("4/statistic   -> statistic")
            print("0/exit      -> Exit")
            print("----------------------------------------------")
            answer = input(">>>>")
            if not answer.isnumeric():
                answer = answer.lower()
            match answer:
                case "stat" | "statistics" | "statistic" | "4":
                    self.showStatistics()
                case "settings" | "options" | "3":
                    self.changeSettings()
                    self.saveSettings()
                case "information" | "info" | "2":
                    print('To start program you have to choose the option named "START" and')
                    print('then program will split your time to "THE WORK TIME" AND ')
                    print('"THE BREAK TIME". You can also change break and work time ')
                    print('by the option named "settings". ')
                    print('Created by Patryk Łata on 21 January 2023')
                case "start" | "learn" | "startlearn" | "1":
                    self.startLearn()
                case "exit" | "quit" | "0":
                    break
                case _:
                    pass

    def __init__(self):
        self.menu()

    def __del__(self):
        self.saveSettings()
        self.saveStatiscs()

Learner()



