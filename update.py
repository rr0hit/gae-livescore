from urllib2 import urlopen
from HTMLParser import HTMLParser
from google.appengine.ext import db
from admin import Whitelists

class LSHTMLParser(HTMLParser):
	'''
	HTMLParse based parser for livescore.com. 
	
	Usage:
	
	>>>parser=LSHTMLParser(whitelist)
	>>>html=urlopen("http://livescore.com").read()
	>>>parser.feed(html)
	>>>ls_teams=parser.teams
	>>>ls_scores=parser.scores
	>>>ls_times=parser.times
	>>>ls_competitions=parser.competitions
	
	whitelist is a list of competitions whose data are
	to be parsed. For Eg:
	whitelist=['England - Premier League', 
			'England - League Championship']
	
	ls_teams is a continuous list of teams. So for eg.
	ls_team[0] is playing against ls_team[1] and so on.	
	'''
	
	def __init__(self, w):
		HTMLParser.__init__(self)
		self.FoundTeam=False
		self.FoundScore=False
		self.FoundTime=False
		self.FoundMatch=False
		self.FoundCompetition=False
		self.FoundDate=False
		self.datacount=0
		self.teams=[]
		self.scores=[]
		self.times=[]
		self.dates=[]
		self.competitions=[]
		self.competition=""
		self.whitelist=w
		self.date=""
			
	def handle_starttag(self, tag, attrs):
		if tag=='td' and ('width', '186') in attrs:
			self.FoundTeam=True
		if tag=='td' and ('width', '51') in attrs:
			self.FoundScore=True
		if tag=='td' and ('width', '45') in attrs and self.FoundMatch:
			self.FoundTime=True
		if tag=='tr' and ('bgcolor',"#dfdfdf") in attrs:
			self.FoundMatch=True
		if tag=='tr' and ('bgcolor',"#cfcfcf") in attrs:
			self.FoundMatch=True
		if tag=='td' and ('class','title') in attrs:
			self.FoundCompetition=True
		if tag=='td' and ('width','423') in attrs:
			self.FoundDate=True
			
	def handle_endtag(self, tag):
		if tag=='td' and self.FoundTeam:
			self.FoundTeam=False
			self.datacount=0
		if tag=='td' and self.FoundScore:
			self.FoundScore=False
		if tag=='td' and self.FoundTime:
			self.FoundTime=False
		if tag=='tr' and self.FoundMatch:
			self.FoundMatch=False
		if tag=='td' and self.FoundCompetition:
			self.competition.strip()
			# livescore.com has added a new table feature in several regions.
			# The string (Table) hence has to be removed from competition name.
			if '(Table)' in self.competition:
				self.competition=self.competition.replace('(Table)','')
				self.competition=self.competition.strip()
			self.FoundCompetition=False
			self.datacount=0
		if tag=='td' and self.FoundDate:
			self.FoundDate=False
			
	def handle_data(self, data):
		#following is some bad code to counter data containing "&" being split. 
		if self.FoundTeam and self.competition in self.whitelist:
			self.datacount=self.datacount+1
			if self.datacount==1:
				self.teams.append(data)
			if self.datacount>1:
				self.teams[-1]=self.teams[-1]+"&"+data
		if self.FoundScore and self.competition in self.whitelist:
			self.scores.append(data)
		if self.FoundTime and self.competition in self.whitelist:
			self.times.append(data)
			self.competitions.append(self.competition)
			self.dates.append(self.date)
		#following is to handle competition name being split into country + competition
		if self.FoundCompetition:
			self.datacount=self.datacount+1
			if self.datacount==1:
				self.competition=data
			if self.datacount>1:
				self.competition=self.competition+data
		if self.FoundDate:
			self.date=data
				
class Matches(db.Model):
	'''
	Datastore entities to store Match data namely
	"home_side", "away_side", "time", "date", 
	"score" and "competition" and a boolean values
	"live" to indicate whether match is in progress
	or not and "finished" to indicate whether match 
	is over or not.
	'''
	home_side = db.StringProperty(required=True, indexed=False)
	away_side = db.StringProperty(required=True, indexed=False)
	time = db.StringProperty(required=True, indexed=False)
	score = db.StringProperty(required=True, indexed=False)
	competition = db.StringProperty(required=True, indexed=False)
	live = db.BooleanProperty(required=True, indexed=False)
	finished = db.BooleanProperty(required=True, indexed=False)
	date = db.StringProperty(required=True, indexed=False)
	
def fetchandstore(url, white):
	html=urlopen(url).read()
	
	#invoke parser		
	parser = LSHTMLParser(white)
	parser.feed(html)

	#get the data
	ls_teams=parser.teams
	ls_scores=parser.scores
	ls_times=parser.times
	ls_competitions=parser.competitions
	ls_dates=parser.dates

	#push new data into datastorage
	for i in range(len(ls_times)):
		m=Matches(home_side=ls_teams[2*i], 
				away_side=ls_teams[2*i+1],
				time=ls_times[i],
				score=ls_scores[i],
				competition=ls_competitions[i],
				date=ls_dates[i],
				live="'" in ls_times[i] or 'HT' in ls_times[i],
				finished='FT' in ls_times[i])
		
		#m.put() does not work for non utf-8 chars in data. Bypassing for now.
		try:
			m.put()
		except UnicodeDecodeError:
			pass

def main():

	#remove previously written data
	results = db.GqlQuery("SELECT * FROM Matches") 
	for r in results:
		db.delete(r)
		
	results = db.GqlQuery("SELECT * FROM Whitelists") 
	for r in results:
		fetchandstore(r.url,r.competitions)
				
if __name__=="__main__":
	main()