#!/usr/bin/python

#Author: Shreesh Kumar Verma
#Mail: tanaykumar103@gmail.com
#Date: 22/09/2021


import os
import datetime as dt
import pickle, argparse

class Helper:
	dateToday = dt.date.today()

	# location of pickle file name 'data' to load
	# change this variable as per requirement
	#data = os.environ['HOME'] + '/.local/arch-updatehelper/data'
	data = os.path.expanduser('~/.local/arch-updatehelper/data')


	def __init__(self):
		
		# Option feature to change difference between days of updates
		parser = argparse.ArgumentParser(description='Options to modify difference between dates')

		# --D optional argument added to change difference
		parser.add_argument('--D', required= False, type=int, help='Value sets difference between dates')
		parser.add_argument('-v', required=False, action='store_true', help='Show next updatable date')

		# add all arguments to parser object
		# self.args contains all the arguments passed and their values.
		self.args = parser.parse_args()


		# checking if any valid --D argument has been passed
		# if True self.writeData() is called and value of diff key is changed
		# else self.main() is called and update is carried on
		if self.args.D is not None:
			self.writeData()

		elif self.args.v is True:
			self.moreInfo()
		else:
			self.main()


	# provided some extra info on next 'updateable-date'
	def moreInfo(self):

		info = self.getData()
		
		# lastDate of update + difference value - today's date,
		# then some string slicing for better output.
		info = str((info[1] + dt.timedelta(info[0])))
		print(f'Next update will be available after {info}')


	# this method retrieves data from pickle file named data stored at location self.data
	# and return's list of [diff,lastDate]
	def getData(self):
		with open(self.data, 'rb') as file:

			data_ = pickle.load(file)

			diff = data_['diff']
			lastDate = data_['lastDate']

		return [diff, lastDate]

	# this method writes to pickle file stored at location self.data
	def writeData(self):
		
		# checking if valid --D argument is passed
		# if true, diff key's value is changed to --D's value
		diff = self.args.D
		if diff is not None and int:
			data_ = {'diff':diff,'lastDate':self.dateToday}	
			print(f'Difference beteen updates changed to {diff}.')
		else:
			# if no --D value is given, original diff values is saved in the pickle file.
			data_ = {'diff':self.getData()[0],'lastDate':self.dateToday}
		file = open(self.data, 'wb')

		pickle.dump(data_, file)
		file.close()

	# lifeline and reason of this whole script.
	# this method actually runs the package manager
	def main(self):

		# retrieve data from pickle file
		info = self.getData()

		# check for difference between date of last update and current date
		# if current date > lastdate then run package manager, else wait.
		if info[1] + dt.timedelta(info[0]) < dt.date.today():
			print('alright... get ready to be updated')
			exit_code = os.system('yay -Syyu')
			
			# conditional to check for exit code of last statement
			# if exit_code == 0, self.writeData() is called else
			# output is generated
			if exit_code == 0:
				self.writeData()
			else:
				print("Failed in updating")
		
		# checking if -v option provided
		# if true, moreinfo() is called
		else:
		#	if self.args.v is True:
		#		self.moreInfo()
			
			print('Wait some time')

if __name__ == '__main__':
	obj = Helper()
