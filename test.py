#!/usr/bin/env python

import urllib2, urllib, sys

request = dict(
	token='xxxxx',
	team_id='T0001',
	channel_id='C2147483705',
	channel_name='test',
	timestamp='1355517523.000005',
	user_id='U2147483697',
	user_name='tester',
	text=' '.join(sys.argv[1:]),
)

print urllib2.urlopen('http://localhost:5000/slack/', urllib.urlencode(request)).read()


