import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Whitelists(db.Model):
	'''
	Database of whitelisted urls and competitions
	'''	
	url = db.StringProperty(required=True)
	competitions = db.StringListProperty()
	
class AdminPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>
			  <h3>Add url and competitions to be whitelisted</h3>
			  <h4>Note:<h4/>
			  <ul>
			  <li>URL must be www.livescore.com links like http://www.livescore.com/soccer/england.<br/>
			  This helps to get schedules of upcoming matches way before matchday. Home page </br>www.livescore.com
			  lists matches only on match day while subpages </br>like the one in example keeps upcoming schedules.
			  </li>
			  <li>Competitions are of form: England - Premier League</li>
			  <li>Multiple competitions can be added by seperating each with a comma.<br/>
			  For Eg. England - Premier League,England - League Two</li>
			  <li>Duplicates will be auto detected and removed.</li>
			  <li>You can view the database in Appspot dashboard > data store viewer</li>
			  </ul>
              <form action="/admin" method="post">
				<div>URL: <input type="text" name="url"/></div>
				<br/>
				Competitions:
                <div><textarea name="competitions" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Add to Whitelist"></div>
              </form>
            </body>
          </html>""")

    def post(self):
		u=cgi.escape(self.request.get('url'))
		c=cgi.escape(self.request.get('competitions')).split(",")
		#remove trailing / from url
		if u[-1]=="/":
			u=u[:-1]
		#check if url already exists	
		results = db.GqlQuery("SELECT * FROM Whitelists WHERE url = :1",u)
		result=results.get()
		if len(results.fetch(1))==0:
			w=Whitelists(url=u,competitions=c)
			w.put()
		else:
			for i in c:
				if i not in result.competitions:
					result.competitions.append(i)
					result.put()

application = webapp.WSGIApplication(
                                     [('/admin', AdminPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()