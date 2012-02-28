Livescore-API
=============

Livescore-API is a Google App Engine application that takes football 
score details from http://www.livescore.com and makes the data available 
to clients in JSON format.

It fetches details of current/upcoming matches and stores them in a 
database and updates the database after a particular time interval.
Only matches of whitelisted competitions listed in competitions.txt
file are tracked. This is to keep resource usage in appspot within
daily limits.

Legality
--------

Usage of the application is completely legal. The FAQ of livescore.com
(http://www.livescore.com/FAQ.htm) states:

	(e-03) Can I copy live score data from your website for my/our own website or other use ?
		   - There is no such law that would prevent you from 
		     doing so, live score data can't be copyrighted as
		     any live score data are factual information and not
		     an invention or intellectual work of somebody. With
		     that in mind however, we do have a mechanism in place
		     to detect and block anybody who would try to copy our
		     content by an automated system, being it crawler, spider
		     or any other automated software.
		 
Configuration
-------------

There are a few bits one can configure before deploying the application.

1. Frequency of updates

Updates are run as cron jobs. Update the cron.yaml appropriately to adjust 
frequency of updates.

2. Completitions to track

Competitions to track are to be added to competitions.txt in a single comma 
separated line without any trailing or preceeding white spaces. Competition
names are of the form "Nation - Competition Name" for eg. "England - League Two" 

Deployment
----------

1. Clone Livescore-Api::

    $git clone git@github.com:rr0hit/Livescore-API.git

2. Register your application at appspot.com

3. Install App Engine Python SDK. (http://code.google.com/appengine/downloads.html)

4. Rename the git directory to the application (for eg. MyApp) name you registered::

	$mv -R Livescore-API MyApp

5. Remove the unwanted files::

	$rm -R MyApp/.git README.rst TODO LICENSE
		
6. Replace the application name in app.yaml::

	$sed  s/Livescore-API/MyApp/ MyApp/app.yaml > MyApp/app.yaml
	
7. Deploy the app::

	$appcfg.py update MyApp
	
Client End Usage Example in Python
----------------------------------
1. All Mathches query:

	>>> from urllib2 import urlopen
	>>> import json
	>>> html=urlopen("http://MyApp.appspot.com/allmatches")
	>>> a=json.load(html)
	>>> for m in a:
	...     print m['time']+" "+m['home_side']+" "+m['score']+" "+m['away_side']
	...	
	19:45 Bury ? - ? Hartlepool U.
	19:45 Macclesfield T. ? - ? Plymouth Argyle
	 53' Elfsborg 0 - 0 Falkenbergs FF
	19:45 Rochdale ? - ? Notts County
	19:45 Morecambe ? - ? Dagenham & R'bridge
	19:45 Barnet ? - ? Bradford C.
	19:45 Gillingham ? - ? Hereford U.
	FT CD Chivas USA 0 - 2 AIK Stockholm
	19:45 Oldham Athletic ? - ? Colchester U.
	19:45 Swindon T. ? - ? Burton
	19:45 Stevenage ? - ? Huddersfield T.
	FT San Jose E'quakes 1 - 1 Portland Timbers
	19:45 Chesterfield ? - ? Charlton Athletic
	19:45 Port Vale ? - ? Crewe Alexandra
	
2. "By teams" query:

	>>> html=urlopen("http://MyApp.appspot.com/byteams?teams=Burton,Gillingham")
	>>> a=json.load(html)
	>>> for m in a:
	...     print m['time']+" "+m['home_side']+" "+m['score']+" "+m['away_side']
	... 
	19:45 Swindon T. ? - ? Burton
	19:45 Gillingham ? - ? Hereford U.
	
3. "By Competitions" query:

	>>> html=urlopen("http://MyApp.appspot.com/bycompetitions?competitions=England%20-%20League%20Two,England%20-%20League%20One")
	>>> a=json.load(html)
	>>> for m in a:
	...     print m['time']+" "+m['home_side']+" "+m['score']+" "+m['away_side']... 
	19:45 Morecambe ? - ? Dagenham & R'bridge
	19:45 Barnet ? - ? Bradford C.
	19:45 Swindon T. ? - ? Burton
	19:45 Port Vale ? - ? Crewe Alexandra
	19:45 Gillingham ? - ? Hereford U.
	19:45 Macclesfield T. ? - ? Plymouth Argyle
	19:45 Stevenage ? - ? Huddersfield T.
	19:45 Bury ? - ? Hartlepool U.
	19:45 Chesterfield ? - ? Charlton Athletic
	19:45 Rochdale ? - ? Notts County
	19:45 Oldham Athletic ? - ? Colchester U.
	
The data parsed also contains a few more fields. Each query as seen above consists of
an array of dictionaries corresponding to individual matches. Each match dict consists
of indices 'home_team', 'away_team', 'score', 'competition' and 'time' which are strings.
There are two additional indices 'finished' and 'live' which are boolean values representing
whether match is finished or ongoing.

LICENSE
-------

This software is licensed under GPL v3. See LICENSE file for details.