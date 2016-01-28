#!/usr/bin/env python

import urllib2
import urllib
import sys

import main

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

event = dict(body=urllib.urlencode(request))

print main.lambda_handler(event, None)
