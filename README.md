# Moodle-Heroku-Attendence-Bot

Bot created for Marking Attendance on Moodle Based Platform and Implemented on Heroku Free Dyno!

## Steps to Deploy Yourself:
1. [Fork This Repository](https://github.com/Amsal1/Moodle-Heroku-Attendence-Bot/fork)
2. Edit timetable.json and users.json as per your needs. 

   Note: If you want to keep your users.json data private, you can download this repo and manually push it to Heroku using Heroku CLI. Make sure you read app.json to know what settings need to be configured with deployment! 

3. Deploy on Heroku: 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
4. Configure the TimeZone while deploying the app through the button or by going to Settings->Config Vars to whatever suits you. By default its set to Asia/Calcutta
5. Edit the users.json and timetable.json as per your needs and then add a Heroku Scheduler Addon to run this python program in the morning at whatever time suits you.

### *Note: The script gets exit after 6pm in evening by default. You can configure that by editing main&#46;py source at line 146*
