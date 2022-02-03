#!/usr/bin/python

# version = 0.2
# date: 21/10/2021

import argparse, os, pickle, gi
import datetime as dt
gi.require_version('Gio','2.0')
from gi.repository import Gio

class AUH:

    '''
    available methods

    1) Change AUR helper -> changeHelper()
    2) Change AUR Command -> changeCommand()
    3) Change Difference between updates -> changeDifferece()
    4) Retrive information from pickle file -> getInfo()
    6) Provide information from pickle -> moreInfo()
    7) Run Updater -> runUpdater()
    8) Write Data -> writeData()
    9) Write post update information -> writeDefault()
    '''

    # multiple use variables
    PickleLocation = os.path.expanduser('~/projects/arch-updatehelper/data')
    #PickleData = {'diff': None,'lastDate': None, 'helper': None,'command': None}
    dateToday = dt.date.today()

    def __init__(self):

        self.info = self.getInfo()

        self.PickleData = {'diff': self.info[0],'lastDate': self.info[1], 'helper': self.info[2],'command': self.info[3]}
        
        
        parser = argparse.ArgumentParser(description='Options to modify difference between dates')

        parser.add_argument('-d', required= False, type=int, help="Value set's difference between dates\nUsage: update -D 3")
        parser.add_argument('-v', action = 'store_true', required=False, help='Show last update date\nUsage: update -V')
        parser.add_argument('-a', required=False, type=str, help='Change AUR helper, Default is yay.\nUsage: update -A yay')
        parser.add_argument('-c', required=False, type=str, help='Customize update command, Default= -Syyu.\nUsage: update -C Syyu')
        parser.add_argument('-n', required=False, action='store_true')

        # add all arguments to parser object
        # self.args contains all the arguments passed and their values.
        self.args = parser.parse_args()

        if self.args.a is not None:
            self.changeHelper()

        elif self.args.c is not None:
            self.changeCommand()

        elif self.args.d is not None:
            self.changeDifference()

        elif self.args.v is True:
            self.moreInfo()

        else:
            self.runUpdater()

    def changeHelper(self):

        helper = self.args.A
        
        self.PickleData['helper'] = helper
        
        try:
            self.writeData()
            print(f'AUR helper changed to: {helper}')

        except:
            print('AUR helper not changed error occured')


    def changeCommand(self):
        
        command = self.args.C
        info = self.getInfo()

        self.PickleData['command'] = '-' + command

        try:
            self.writeData()
            print(f'Command changed to: {command}')

        except:
            print('Command not changed error occured')


    def changeDifference(self):
        
        diff = self.args.d
        info = self.getInfo()
        
        self.PickleData['diff'] = diff

        try:
            self.writeData()
            print(f'Difference changed to: {diff}')

        except:
            print('Difference not changed error occured')


    def getInfo(self):
        
        try:
            with open(self.PickleLocation, 'rb') as PickleFile:
                data = pickle.load(PickleFile)

                diff = data['diff']
                lastDate = data['lastDate']
                helper = data['helper']
                command = data['command']

            return [diff, lastDate, helper, command]
        
        except:
            print ('Error in retrieving info')

    
    def moreInfo(self):
        
        info = self.getInfo()
        nextDate = dt.timedelta(days=info[0]) + info[1]
        output = f'''Difference: {info[0]}.\nNext update on: {nextDate}.\nCurrent helper: {info[2]}.\nCommand used: {info[3]}'''

        print(output)


    def notifier(self, exitcode):

        Application = Gio.Application.new("update.notifier", Gio.ApplicationFlags.FLAGS_NONE)
        Application.register()
        Notification = Gio.Notification.new("Updater")
        Icon = Gio.ThemedIcon.new("dialog-information")
        Notification.set_icon(Icon)
        #Application.send_notification(None, Notification)
        if exitcode == 0:
            Notification.set_body('Update executed with exit code 0; check output file\n at $HOME/updatelog.txt')
        elif exitcode == 2:
            Notification.set_body('Update executed with exit code 2; Wait some time.')
        else:
            Notification.set_body('Update failed with exit code 1; check output file\n at $HOME/updatelog.txt')
        Application.send_notification(None, Notification)


    def runUpdater(self):
        
        # retrieve data from pickle file
        info = self.getInfo()

        # check for difference between date of last update and current date
        # if current date > lastdate then run package manager, else wait.
        if info[1] + dt.timedelta(days=info[0]) < self.dateToday:
            print('alright... get ready to be updated')
           # try:
           #     os.system('rm $HOME/updatelog.txt')
           # except:
           #     pass
            
            exit_code = os.system(f'sudo {info[2]} {info[3]} --noconfirm')
            
            # conditional to check for exit code of last statement
            # if exit_code == 0, self.writeData() is called else
            # output is generated
            if exit_code == 0:
                self.writeDefault()
                print(f'Exit Code: {exit_code}')
    
                # check if -n is provided   
                if self.args.n:
                    self.notifier(exit_code)
            else:
                print("Failed in updating")

            
        else:
            self.notifier(exitcode=2)
            print('Wait some time')

    
    def writeData(self):
        try:
            with open(self.PickleLocation, 'wb') as PickleFile:
                pickle.dump(self.PickleData, PickleFile)

        except:
            print('Error in writing data')


    def writeDefault(self):
        helper = self.args.a
        info =self.getInfo()

        self.PickleData['lastDate'] = self.dateToday
       
        try:
            self.writeData()
            print('Update information saved')

        except:
            print('Update information not saved error occured')

if __name__ == '__main__':
    AUH()
