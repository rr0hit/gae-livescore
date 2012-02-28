from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import simplejson as json
from google.appengine.ext import db
from update import Matches

class GetscoreByTeams(webapp.RequestHandler):
	'''
	RequestHandler class for /byteams page. Outputs
	a JSON array of all the teams' score details.
	'''
	def _handlerequest(self):
		self.t=self.request.get('teams')
		self.output=[]
		self.teamlist=self.t.split(',')
		for tm in self.teamlist:
			self.result=db.GqlQuery("SELECT * "
									"FROM Matches "
									"WHERE home_side = :1",
									tm)
		
			for r in self.result:
				self.output.append({'home_side':r.home_side,
									'away_side':r.away_side,
									'score':r.score,
									'time':r.time,
									'competition':r.competition,
									'live':r.live,
									'finished':r.finished})
								
			self.result=db.GqlQuery("SELECT * "
									"FROM Matches "
									"WHERE away_side = :1",
									tm)
		
			for r in self.result:
				self.output.append({'home_side':r.home_side,
									'away_side':r.away_side,
									'score':r.score,
									'time':r.time,
									'competition':r.competition,
									'live':r.live,
									'finished':r.finished})
								
		self.response.out.write(json.dumps(self.output))
	def get(self):
		self._handlerequest()

class GetscoreByCompetitions(webapp.RequestHandler):
	'''
	RequestHandler class for /bycompetitions page. 
	Outputs a JSON array of score details of all
	matches in a competition.
	'''
	def _handlerequest(self):
		self.c=self.request.get('competitions')
		self.output=[]
		self.competitions=self.c.split(',')
		for ct in self.competitions:
			self.result=db.GqlQuery("SELECT * "
									"FROM Matches "
									"WHERE competition = :1",
									ct)
		
			for r in self.result:
				self.output.append({'home_side':r.home_side,
									'away_side':r.away_side,
									'score':r.score,
									'time':r.time,
									'competition':r.competition,
									'live':r.live,
									'finished':r.finished})
								
		self.response.out.write(json.dumps(self.output))
	def get(self):
		self._handlerequest()

class GetMatches(webapp.RequestHandler):
	'''
	RequestHandler class for /allmatches page. Outputs
	a JSON array of score details of all matches.
	'''
	def _handlerequest(self):
		self.output=[]

		self.result=db.GqlQuery("SELECT * "
								"FROM Matches "
								)
		for r in self.result:
			self.output.append({'home_side':r.home_side,
									'away_side':r.away_side,
									'score':r.score,
									'time':r.time,
									'competition':r.competition,
									'live':r.live,
									'finished':r.finished})
								
		self.response.out.write(json.dumps(self.output))
	def get(self):
		self._handlerequest()
				
application = webapp.WSGIApplication(
                                     [('/byteams', GetscoreByTeams), 
									 ('/bycompetitions',GetscoreByCompetitions),
									 ('/allmatches',GetMatches)],
                                     debug=True)
def main():
	run_wsgi_app(application) 

if __name__ == "__main__":
	main()