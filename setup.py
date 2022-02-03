#!/usr/bin/python

# Author: Shreesh Kumar Verma
# Email: tanaykumar103@gmail.com
# Date: 12/10/2021
# Purpose: Installer and setup script for arch-updatehelper


import os, pickle, argparse
import datetime as dt


# CLI arguments setup
parser = argparse.ArgumentParser(description='Option to remove arch-updatehelper script')
parser.add_argument('--R', required=False,action='store_true', help='Use to remove files related to arch-updatehelper script')

args = parser.parse_args()



# prepares the pickle file for usages
def pickle_prep():

	# location of pickle file
	fileLoc = os.path.expanduser('~/.local/arch-updatehelper/data')
	
	# data to initiate pickle file
	data = {'diff':3,'lastDate':dt.date.today(), 'helper': 'pacman','command':'-Syu'}
	
	# finally writing the file at location <fileLoc>
	with open(fileLoc, 'wb') as file:
		pickle.dump(data, file)


# places all the necessary files to the location <fileLoc>
def place_files():

	# makes the required directory if already not present
	os.system('mkdir -p ~/.local/arch-updatehelper/')

	pwd = os.getcwd()
	
	# location of file to place at
	fileLoc = os.path.expanduser('~/.local/arch-updatehelper/')
	
	# finally copying files to <fileLoc>
	os.system(f'cp {pwd}/update.py {fileLoc}')

	# adding alias to ~/.bashrc
	os.system('''echo "alias update='python $HOME/.local/arch-updatehelper/update.py'" >> $HOME/.bashrc''')
	print('Alias added to ~/.bashrc as update')

	#sourcing ~/.bashrc to load alias
	os.system('source ~/.bashrc')

# just incase you don't want me anymore
def uninstall():

	# directory location containing all files at <fileLoc>
	fileLoc = os.path.expanduser('~/.local/arch-updatehelper/')
	
	# file location to remove from
	os.system(f'rm -rf {fileLoc}')


if __name__ == '__main__':


	# if --R provided, removes the arch-updatehelper script
	if args.R:
		try:
			print('Removing the arch-updatehelper script')	
			uninstall()
			print('Script removed, thanks for trying...')
		except:
			print('Script not removed...')	
	
	# if --R not provided, place all the necessary files
	else:
		try:
			print('Starting with installation')
			place_files()
			pickle_prep()
			print('All files placed where they should be \n'
				'At ~/.local/arch-updatehelper/')
		except:
			print('error in setting up files')
