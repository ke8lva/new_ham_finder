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
found_email = ['youremail@email.com']
none_found_email = ['anotheremail@email.com']
#email you want reciever of these emails to reply to if they reply.
reply_address = 'email@email.com'
#location where you want FCC file to be saved. If your path starts C:\Users use / not \
zip_location = 'path/to/your/file/location'
#Desired zip code areas to search for new hams.
zip_list = ['44691', '44667', '44662', '44230', '44606', '44270', '44287',
 '44618', '44627', '44624', '44676', '44217', '44677', '44666', '44645',
  '44214', '44276', '44636', '44659']
#smtp email server setting
port = 587
smtp_server = 'smtp.mail.server'
sender_email = 'smtp@domain.com'
password = ''


"""
No changes need to be made below here.
"""

#lists to be built by the program
newCall_list = []
county_list = []
final_list = []
desired_dates = []
index = 1
index2 = 0
email_message = ''
today = datetime.now()
pid = os.getpid()
#Download and unzip weekly FCC database
url = "https://data.fcc.gov/download/pub/uls/complete/l_amat.zip"
filename = url.split('/')[-1]
response = requests.get(url)
zipfile = zipfile.ZipFile(BytesIO(response.content))
zipfile.extractall(zip_location)
response.close()
#Send email function
def email(address):
    message = f'Here are the new hams in Wayne County for {desired_dates[-1]} - {desired_dates[0]}.\n\n{email_message}'
    msg = MIMEText(message)
    msg['Subject'] = f'New Hams {desired_dates[-1]} - {desired_dates[0]}'
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
for d in range(7):
    i = today - timedelta(days = index2)
    desired_dates.append(i.strftime("%m/%d/%Y"))
    index2 += 1
# Get desired rows from "HS" file
with open(f'{zip_location}/HS.dat', 'r') as hs_data:
    hs_reader = csv.reader(hs_data, delimiter='|')
    for row in hs_reader:
        if row[5] == 'SYSGRT' and row[4] in desired_dates:
            newCall_list.append(row)
        else:
            continue
#Get desired rows from "EN" file
with open(f'{zip_location}/EN.dat', 'r') as en_data:
    en_reader = csv.reader(en_data, delimiter='|')
    for row in en_reader:
        if row[18][0:5] in zip_list:
            county_list.append(row)
        else:
            continue
# Compare built lists and compile new list of ones that match
for x in county_list:
    for y in newCall_list:
        if x[4] == y[3]:
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
    email(none_found_email)
    print('No new hams')
    exit()