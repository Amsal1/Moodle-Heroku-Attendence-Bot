# Moodle-Heroku-Attendence-Bot

Bot created for marking Attendance and implemented on Heroku Free Dyno!

## Steps to Deploy Yourself:
1. Deploy on Heroku through this button: 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
2. Configure the TimeZone while deploying the app through the button or by going to Settings->Config Vars to whatever suits you. By default its set to Asia/Calcutta
3. Edit the users.json and timetable.json as per your needs and then add a Heroku Scheduler Addon to run this python program in the morning at whatever time suits you.
*Note: Its gets auto off after 6pm in evening by default. You can configure that by editing main.py source*
