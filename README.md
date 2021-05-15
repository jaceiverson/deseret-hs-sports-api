# deseret-hs-sports-api

Created a simple API for <a href=https://sports.deseret.com/high-school>Deseret News High School Sports</a> section.

This is in its infancy right now, but will be improved as i work on it more. 

Currently, there is a class DSS - Deseret Sports Scraper - that accepets a Deseret url in the following format:
```
https://sports.deseret.com/high-school/school/{school-name}/{sport}/scores-schedule
```
The default functionality is using the module after initalizing the DSS object:
```
self.run()
```
This scrapes the site and pull a date and the date previous's results as well as upcoming games. It then sends an email to all emails listed in the recipients.txt file.

NOTE: This defaults to datetime.date.today(), but can be changed using the module: 
```
self._set_date(new_date)
```
## Example
You can find an example of what was done in the **example_fhs.py** file. 

### Email/Config File Requirements
I have writen a send_email module that relies on a make_config module that I also created.
You can find these here: https://github.com/jaceiverson/custom-python<br>

Details on how to best use these modules is inclued on the README.md for that project.

## Recomended Automation
#### MAC
Use crontab. One of the best articles on how to set up crontab working on your mac can be found here:<br>
https://www.jcchouinard.com/python-automation-with-cron-on-mac/#troubleshooting
#### Windows
Use the Task Scheuler. A clear article on how to do this can be found here:<br>
https://www.jcchouinard.com/python-automation-using-task-scheduler/
