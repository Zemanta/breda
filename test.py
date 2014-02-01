#!/usr/bin/env python

import urllib2, urllib, sys, authsettings

request = dict(
	token=authsettings.AUTH_TOKEN,
	team_id='T0001',
	channel_id='C2147483705',
	channel_name='test',
	timestamp='1355517523.000005',
	user_id='U2147483697',
	user_name='tester',
	text=' '.join(sys.argv[1:]),
)

print urllib2.urlopen('http://localhost:3201/msg/', urllib.urlencode(request)).read()

