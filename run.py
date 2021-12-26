import requests
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 0
HOST = ""
EMAIL_ADDRESS = ""
PASSWORD = ""
API_KEY=""
TODAY = datetime.today().strftime('%Y-%m-%d')

with open('config.json') as json_file:
    data = json.load(json_file)
    PORT = data["email"]["port"]
    HOST = data["email"]["host"]
    EMAIL_ADDRESS = data["email"]["email_address"]
    PASSWORD = data["email"]["password"]
    API_KEY = data["apikey"]
    



url = "https://api-basketball.p.rapidapi.com/games"
querystring = {"date":TODAY}
headers = {
    'x-rapidapi-host': "api-basketball.p.rapidapi.com",
    'x-rapidapi-key': API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)


with open('datas/today_matches.json', 'w') as f:
    f.write(response.text)





class Match:
    def __init__(self, date, time, home, away):
        self.date =date
        self.time = time
        self.home = home
        self.away = away
        
    def toJSON(self):
        return {
            "date":self.date,
            "time": self.time,
            "home":self.home,
            "away":self.away
        }
        

with open('datas/today_matches.json') as json_file:
    data = json.load(json_file)
    for match in data['response']:
        if match['league']['id']==12:
            nba_match = Match(match['date'],match['time'],match['teams']['home']['name'], match['teams']['away']['name'])
            print(nba_match.toJSON())


'''
Here comes the email sending --->
'''

html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
    <p>{length} - {ordinal}</p>
  </body>
</html>
""".format(length='multi-line', ordinal='second')


with smtplib.SMTP(host=HOST, port=PORT) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, PASSWORD)
    '''
    subject = 'Szia Zita ra ersz holnap'
    body = 'Tok jo lenne egyet ebedelni'
    msg = f'Subject: {subject}\n\n{body}'
    '''
    message = MIMEMultipart("alternative")
    message["Subject"] = TODAY + " napi NBA - meccsek"
    
    part2 = MIMEText(html, "html")
    message.attach(part2)
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
