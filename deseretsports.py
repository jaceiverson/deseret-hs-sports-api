import requests as r
from bs4 import BeautifulSoup
import datetime as dt
import dateutil.parser as dparser
#custom modules
#https://github.com/jaceiverson/custom-python
from custompython.send_email import send
from custompython.make_config import read

class DSS():
    '''
    Desseret Sports Scrape

    pulls scores for any sport and sends an email with today & yesterday's scores
    as well as the upcoming games

    pass in a url with the following format:
    https://sports.deseret.com/high-school/school/{school-name}/{sport}/scores-schedule


    today can be overwritten using the self._set_date(new_date) method
    '''
    def __init__(self,url):
        self.date = dt.date.today()
        self.team_name = ' '.join(url.split('school/')[-1].split('/')[:2]).title()

        self.base_url = 'https://sports.deseret.com'
        self.raw = r.get(url)
        self.soup = BeautifulSoup(self.raw.text, 'html.parser')
        self.soup_scores = self.soup.find_all('tr')
        self.soup_cards = self.soup.find_all('table',
                                             class_='GameCard_gameCard__3NUB1')
        self.soup_details = self.soup.find_all('div',
                                               class_='GameCard_links__2z5ji')

    def _set_date(self,date):
        self.date = date

    def win_or_lose(self,game_str):
        game = game_str.split('@')
        t1 = game[0]
        t2 = game[1]
        team1_name = ' '.join(t1.split(' ')[:-1])
        team2_name = ' '.join(t2.split(' ')[:-1])
        #penalty check
        if '(' in t1:
            team1_score = int(t1.split(' ')[-1].split('(')[0])
            team2_score = team1_score
            t1_p = t1[t1.find('(')+1 : t1.find(')')]
            t2_p = t2[t2.find('(')+1 : t2.find(')')]
            if t1_p > t2_p:
                return '{} defeated {} in penalties. '\
                        'Game score: {}:{} Penalty score: {} to {}' \
                    .format(team1_name, \
                            team2_name, \
                            team1_score, \
                            team2_score,
                            t1_p,
                            t2_p)
            elif t1_p < t2_p:
                return '{} defeated {} in penalties. '\
                       'Game score: {}:{} Penalty score: {} to {}' \
                    .format(team2_name, \
                            team1_name, \
                            team2_score, \
                            team1_score,
                            t2_p,
                            t1_p)
            elif team2_score > team1_score:
                return '{} defeated {} by a score of {} to {}' \
                    .format(team2_name, \
                            team1_name, \
                            team2_score, \
                            team1_score)
        else:
            team1_score = int(t1.split(' ')[-1])
            team2_score = int(t2.split(' ')[-1])
            if team1_score > team2_score:
                return '{} defeated {} by a score of {} to {}' \
                    .format(team1_name, \
                            team2_name, \
                            team1_score, \
                            team2_score)
            elif team2_score > team1_score:
                return '{} defeated {} by a score of {} to {}' \
                    .format(team2_name, \
                            team1_name, \
                            team2_score, \
                            team1_score)
            else:
                return '{} TIED {} by a score of {} to {}' \
                    .format(team1_name, \
                            team2_name, \
                            team1_score, \
                            team2_score)
    def scrape(self):
        '''
        navigates through the soup objects that were already pulled
        to get the scores
        '''
        today = ''
        yesterday = ''
        upcoming = ''
        for card in self.soup_cards:
            game = card.contents
            for scores in game:
                if 'Final' in scores.text:
                    parsed_date = dparser.parse(scores.text.split('Final')[1],
                                                fuzzy=True).date()
                    if parsed_date == self.date:
                        today +=  self.win_or_lose(game[game.index(scores)+1].text) +\
                                   '\n'
                        today += 'Details here: ' +\
                                   self.base_url +\
                                   self.soup_details[self.soup_cards.index(card)]\
                                        .find('a', href=True)['href']
                    elif parsed_date == self.date - dt.timedelta(days=1):
                        yesterday += self.win_or_lose(game[game.index(scores)+1].text) +\
                                    '\n'
                        yesterday += 'Details here: ' +\
                                   self.base_url +\
                                   self.soup_details[self.soup_cards.index(card)]\
                                        .find('a', href=True)['href']
                if 'Upcoming' in scores.text:
                    upcoming += game[game.index(scores)+1].text +\
                               ' on ' +\
                               scores.text.split('Upcoming')[1]
        if today == '':
            today = "No Games"
        if yesterday == '':
            yesterday = 'No Games'
        if upcoming == '':
            upcoming = 'No Games'

        return today,yesterday, upcoming

    def _pull_rec(self,file_path = 'recipients.txt'):
        '''
        pulls the recipients of the email from the given filepath
        defaults to recipients.txt
        '''
        rec = ''
        with open(file_path,'r') as f:
            rec+=f.read()
        if isinstance(rec,list):
            return rec.split('\n')
        elif isinstance(rec,str):
            return [rec]

    def email(self,sub,msg):
        '''
        subject: str: what the subject of the email is
        msg: str:
        sends the email
        '''
        config = read()
        rec = self._pull_rec()
        sender = self.team_name + '-updates@gmail.com'
        send(sub,[msg],[rec],sender,config)

    def run(self):
        td,ys,up = self.scrape()
        msg = ["::GAME REPORT::\n",
                "TODAY:\n{}\n".format(td),
                "YESTERDAY:\n{}\n".format(ys),
                "UPCOMING:\n{}".format(up)
               ]
        sub = self.team_name + ' Update'
        self.email(sub,msg)