
# New Ham Finder

New ham finder is a simple program that finds newly licensed amateur radio operators by your 
defined zipcodes using the FCC database uploads, then emails you their information.  It 
excludes any previously licensed operators that upgraded and chose to receive a new 
systematic callsign as well as exclude new club call signs.  The repository includes two 
version; newhams_daily and newhams_weekly.  They give the same results but one should be 
executed once per week and uses the fcc weekly uploads and the other should be executed 
daily and uses the FCC daily uploads.


## Prerequisites
Python3 or greater

## Installation

Naviagte to the directory you want the repository saved.  
 **cd /etc** 

Download the repository  
**sudo git clone https://github.com/ke8lva/new_ham_finder.git**

You will need to choose if you want to use the daily or weekly version.  They require the
same setup. For this I will use newhams_daily.py

Use an editor to edit the file.\
**sudo nano /etc/new_ham_finder/newhams_daily.py**

You will need to change your information in the variables towards the top.  

found_email and none_found_email are the addresses you want the program to send the final
results to.  They can be the same or different addresses.  To send to multiple email
addresses, seperate the emails in quotes with a comma.This will all be inside of the square 
brackets Example: ``['example1@email.com', 'example2@email.com']`` best practice is to have a 
space after the comma.  
 __found_email = ``['anemail@email.com']``__  
 __none_found_email = ``['anotheremail@email.com']``__

reply_address is the email address you would want someone to respond to if they do. This
can be the same or different as sender_email.  
**reply_address = ``'yourreplytoaddress@email.com'``**

Desired zip code areas to search for new hams. This can be as few or as many as you would
like. Make sure to follow the same format as below.  zipcodes in quotes seperate by a
comma and space.  All inside the square brackets.  
__zip_list = ['44691', '44667', '44662', '44230', '44606', '44270', '44287',  
'44618', '44627', '44624', '44676', '44217', '44677', '44666', '44645',  
'44214', '44276', '44636', '44659']__

This is where all of your smtp email host setting will go. For this I will use gmail as an
example. You can find your email providers smtp settings with a quick internet search  
__port = 587__  
__smtp_server = 'smtp.gmail.com'__  
__sender_email = ``'yourgmail@gmail.com'``__  
__password = 'yourpassword'__

*Starting June 2022 gmail no longer supports "less secure apps" for smtp.  If you are using
gmail, you will have to obtain an app password from gmail.  Once you get this, you will
use your app password in place of you email password for this script.*

You can find instruction to receive an app password below.  
__<https://support.google.com/mail/answer/185833?hl=en>__

If you do not want to receive an email if no new hams where found you can simply comment
this line out towards the bottom of the script, like below.  
__#     email(none_found_email)__

Save your changes  
__ctrl + o__  
__hit enter__  
exit the editor  
__ctrl + x__  

To test that it is functioning, from the directory that newhams_daily.py is located, simply  
execute the follow  
**python newhams_daily.py**  

This should excute quickly and send you an email. 

Next you will need to schedule the newhams_daily.py to run when you want.  Open crontab
to set the schedule.  
__crontab -e__  

I will schedule this to run every day at 6:00 am with the below line. for newhams_weekly you would  
schedule it to run once per week.
**0 6 * * * /usr/bin/python3 /etc/new_ham_finder/newhams_daily.py**  

Save and exit  
**ctrl + o**  
**enter**  
**ctrl + x**

    
## License

[GNU General Public License v3.0](https://github.com/ke8lva/new_ham_finder/blob/main/LICENSE)

