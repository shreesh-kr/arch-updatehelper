# arch-updatehelper
**A simple python script to help people(arch/ arch-based) with update habit.**

**INSTALLATION**  
run the setup.py file and it will handle all the work  
PS: Files are placed in $HOME/.local/arch-updatehelper  
To **Uninstall** use:  
$> setup.py --R  

**USAGE**  
To run from terminal simply type _update_ and it will start its work.
If any changes in the file location are made, direct changes in the update.py file are necessary as per requirement.

**Sample usage:**  
**To simply run script**  
$> update  
**To change difference between to dates to 3 days**  
$> update --D 3  
**To check for more information use the following option**  
$> update -v  
**To change AUR helper**  
$> update --A _helpername_
