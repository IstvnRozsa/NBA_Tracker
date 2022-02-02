import requests
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

PORT = 0
HOST = ""
EMAIL_ADDRESS = ""
PASSWORD = ""
API_KEY=""
TODAY = datetime.today().strftime('%Y-%m-%d')

with open(os.path.expanduser('~/Projects/nba-tracker/config.json')) as json_file:
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


with open(os.path.expanduser('~/Projects/nba-tracker/datas/today_matches.json'), 'w') as f:
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
    def toHTML(self):
        return """\
            <h2>{home} VS. {away}</h2>
            <ul>
                <li>Kezdés: {time}</li>
            </ul>
            """.format(home = self.home, away = self.away, time = self.time)
        
matches_html = ""
with open(os.path.expanduser('~/Projects/nba-tracker/datas/today_matches.json')) as json_file:
    data = json.load(json_file)
    
    for match in data['response']:
        if match['league']['id']==12:
            nba_match = Match(match['date'],match['time'],match['teams']['home']['name'], match['teams']['away']['name'])
            matches_html += nba_match.toHTML()
            print(nba_match.toJSON())


'''
Here comes the email sending --->
'''

html = '''\
<html>
  <body>
    <h1>NBA Games - {date}</h1>
    <p>
    These teams are playing tonight.
    Have fun!
    </p>
    
    {matches}
    
    <a href="https://www.nba.com>"Check out more info..</a> 
  </body>
</html>
'''.format(date=TODAY, matches=matches_html)


with smtplib.SMTP(host=HOST, port=PORT) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_ADDRESS, PASSWORD)
    
    message = MIMEMultipart("alternative")
    message["Subject"] = TODAY + " today's NBA matches"
    
    part2 = MIMEText(html, "html")
    message.attach(part2)
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())
