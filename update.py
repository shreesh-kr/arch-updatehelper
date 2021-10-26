# version = 0.2
# date: 21/10/2021

import argparse, os, pickle
import datetime as dt


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
    PickleLocation = os.path.expanduser('~/projects/arch-updatehelper/test/data')
    #PickleData = {'diff': None,'lastDate': None, 'helper': None,'command': None}
    dateToday = dt.date.today()

    def __init__(self):

        self.info = self.getInfo()

        self.PickleData = {'diff': self.info[0],'lastDate': self.info[1], 'helper': self.info[2],'command': self.info[3]}
        
        
        parser = argparse.ArgumentParser(description='Options to modify difference between dates')

        parser.add_argument('-D', required= False, type=int, help="Value set's difference between dates\nUsage: update -D 3")
        parser.add_argument('-V', action = 'store_true', required=False, help='Show last update date\nUsage: update -V')
        parser.add_argument('-A', required=False, type=str, help='Change AUR helper, Default is yay.\nUsage: update -A yay')
        parser.add_argument('-C', required=False, type=str, help='Customize update command, Default= -Syyu.\nUsage: update -C Syyu')


        # add all arguments to parser object
        # self.args contains all the arguments passed and their values.
        self.args = parser.parse_args()

        if self.args.A is not None:
            self.changeHelper()

        elif self.args.C is not None:
            self.changeCommand()

        elif self.args.D is not None:
            self.changeDifference()

        elif self.args.V is True:
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
        
        diff = self.args.D
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

        output = f'''Difference: {info[0]}.\nLast updated on: {info[1]}.\nCurrent helper: {info[2]}.\nCommand used: {info[3]}'''

        print(output)


    def runUpdater(self):
        
        # retrieve data from pickle file
        info = self.getInfo()

        # check for difference between date of last update and current date
        # if current date > lastdate then run package manager, else wait.
        if info[1] + dt.timedelta(days=info[0]) < self.dateToday:
            print('alright... get ready to be updated')
            exit_code = os.system(f'sudo {info[2]} {info[3]}')
            
            # conditional to check for exit code of last statement
            # if exit_code == 0, self.writeData() is called else
            # output is generated
            if exit_code == 0:
                self.writeDefault()
                print(f'Exit Code: {exit_code}')
            else:
                print("Failed in updating")

        else:
            print('Wait some time')

    
    def writeData(self):
        try:
            with open(self.PickleLocation, 'wb') as PickleFile:
                pickle.dump(self.PickleData, PickleFile)

        except:
            print('Error in writing data')


    def writeDefault(self):
        helper = self.args.A
        info =self.getInfo()

        self.PickleData['lastDate'] = self.dateToday
       
        try:
            self.writeData()
            print('Update information saved')

        except:
            print('Update information not saved error occured')

if __name__ == '__main__':
    AUH()
