import requests, zipfile, csv, smtplib, ssl, os
from io import BytesIO
from datetime import datetime, timedelta
from email.utils import formatdate
from email.mime.text import MIMEText

"""
Start of user defined variables.  Make necessary adjusments here.
"""

#Email addresses that the program should send to if new hams are or are not found.
# Multiple email seperated by , Example: 'example@mail.com', 'example2@mail.com'
found_email = ['anemail@email.com']
none_found_email = ['anotheremail@email.com']
#email you want reciever of these emails to reply to if they reply.
reply_address = 'yourreplytoaddress@email.com'
#Desired zip code areas to search for new hams.
zip_list = ['44691', '44667', '44662', '44230', '44606', '44270', '44287',
 '44618', '44627', '44624', '44676', '44217', '44677', '44666', '44645',
 '44214', '44276', '44636', '44659']
#your smtp email server setting
port = 587
smtp_server = 'smtp.mail.server'
sender_email = 'youremail@email.com'
password = 'yourpassword'
working_directory = '/path/to/working/directory'

"""
No changes need to be made below here.
"""

#lists to be built by the program
newCall_list = []
county_list = []
final_list = []
upgrade_list = []
index = 1
email_message = ''
today = datetime.now()
yesterday = datetime.today() - timedelta(days=1)
desired_dates = yesterday.strftime('%m/%d/%Y')
day = ''
pid = os.getpid()
# assign day of week to day variable for getting correct download
if datetime.today().weekday() == 0:
    day = 'sun'
elif datetime.today().weekday() == 1:
    day = 'mon'
elif datetime.today().weekday() ==2:
    day = 'tue'
elif datetime.today().weekday() == 3:
    day = 'wed'
elif datetime.today().weekday() == 4:
    day = 'thu'
elif datetime.today().weekday() == 5:
    day = 'fri'
elif datetime.today().weekday() == 6:
    day = 'sat'
else:
    exit()
#Download and unzip weekly FCC database
url = f'https://data.fcc.gov/download/pub/uls/daily/l_am_{day}.zip'
filename = url.split('/')[-1]
response = requests.get(url)
zipfile = zipfile.ZipFile(BytesIO(response.content))
zipfile.extractall(working_directory)
response.close()
#Send email function
def email(address):
    message = f'Here are the new hams in your area for {desired_dates}.\n\n{email_message}'
    msg = MIMEText(message)
    msg['Subject'] = f'New Hams {desired_dates}'
    msg['From'] = sender_email
    msg['To'] = ', '.join(address)
    msg['Reply-To'] = reply_address
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = f'<{today.strftime("%Y%m%d%H%M%S")}.{pid}@{smtp_server}>'
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, address, msg.as_string())
#Build desired date range
with open(f'{working_directory}/HS.dat', 'r') as hs_data: 
    temp_list = []
    hs_reader = csv.reader(hs_data, delimiter='|')
    for i in hs_reader:
        temp_list.append(i)
#Get desired date range data from rows in HS file 
    for row in temp_list:
        if row[5] == 'SYSGRT' and row[4] == desired_dates:
            newCall_list.append(row)
        else:
            continue        
#Get desired rows from "EN" file
with open(f'{working_directory}/EN.dat', 'r') as en_data:
    en_reader = csv.reader(en_data, delimiter='|')
    for row in en_reader:
        if row[18][0:5] in zip_list:
            county_list.append(row)
        else:
            continue
#Get data from AM file to see if they are a ham that upgraded and recieved a 
# new systematic callsign and that it is not a club callsign.
with open(f'{working_directory}/AM.dat', 'r') as am_data:
    am_reader = csv.reader(am_data, delimiter='|')
    for row in am_reader:
        for i in newCall_list:
            if row[4] == i[3] and row[17] == '':
                upgrade_list.append(row)
            else:
                continue
# Compare built lists and compile new list of ones that match
for x in county_list:
    for y in upgrade_list:
        if x[4] == y[4] and y[15] == '':
            final_list.append(x)
        else:
            continue
#Build email message
if len(final_list) > 0:
    for b in final_list:
        email_message += f'{str(index)}\n\
        Callsign: {b[4]}\n\
        First Name: {b[8]}\n\
        Last Name: {b[10]}\n\
        Address: {b[15]}\n\
        P.O. Box: {b[19]}\n\
        City: {b[16]}\n\
        State: {b[17]}\n\
        Zip: {b[18]}\n\n'
        index += 1
    email(found_email)
    print(email_message)
    exit()
else:
    email_message += 'There are no new hams for this date range.'
#if you dont want to receive an email if none where found comment out the next line
    email(none_found_email)
    print('No new hams')
    exit()
