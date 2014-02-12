#!/usr/bin/env python

import json, authsettings, os, traceback, urllib2, urllib, re

import flask
app = flask.Flask(__name__)

import handlers
import smartass


def _post_message(username, channel, text, parse='none'):
	args = dict(
		token=authsettings.POST_TOKEN,
		channel=channel,
		text=text,
		username=username,
		pretty='1',
		parse=parse,
		link_names='1',
	)
	urllib2.urlopen('https://slack.com/api/chat.postMessage', urllib.urlencode(args))


@app.route('/msg/', methods=['POST'])
def process_message():
	if flask.request.form.get('token') != authsettings.AUTH_TOKEN:
		flask.abort(403)
	user = flask.request.form.get('user_name')
	chan = flask.request.form.get('channel_name')
	message = flask.request.form.get('text').encode('utf-8').split()
	try:
		if hasattr(handlers, message[1].lower()):
			return json.dumps(dict(text=getattr(handlers, message[1].lower())(user, chan, message)))
		else:
			return json.dumps(dict(text=smartass.replay(message)))
	except:
		return json.dumps(dict(text="Oh, bummer: " + traceback.format_exc()))


@app.route('/push/', methods=['POST'])
def push():
	data = json.loads(flask.request.form.get('payload', {}))
	if not data:
		return ''
	os.system('git pull')
	os.system('supervisorctl restart breda')
	return 'OK'


@app.route('/seyren/', methods=['POST'])
def relay_seyren():
	check = flask.request.json.get('check')
	check_url = 'http://seyren.zemanta.com/#/checks/%s' % check.get('id')
	check_name = check.get('name', '')
	check_desc = check.get('description', '')
	subs = check.get('subscriptions', [])
	nicks = ''
	for sub in subs:
		if sub.get('type') == 'IRCCAT':
			nicks = sub.get('target') + ' '
			break
	preview = flask.request.json.get('preview')
	try:
		chart_url = re.findall(r'img src=(.*)></img>$', preview)[0]
	except:
		chart_url = ''
	alerts = flask.request.json.get('alerts', [])
	for alert in alerts:
		from_type = alert.get('fromType', 'unknown')
		to_type = alert.get('toType', 'unknown')
		value = alert.get('value', 0)
		error = alert.get('error', 0)
		warn = alert.get('warn', 0)
		if to_type == 'OK':
			emo = 'smile'
		elif to_type == 'WARN':
			emo = 'angry'
		elif to_type == 'ERROR':
			emo = 'rage'
		else:
			emo = 'confused'
		_post_message('seyren', '#devops', '%(nicks)s<%(check_url)s|%(check_name)s> changed from %(from_type)s to %(to_type)s, value was %(value)s (warn: %(warn)s, crit: %(error)s) :%(emo)s:' % vars())
		if chart_url:
			_post_message('seyren', '#devops', '<%s|check chart>' % chart_url)
	return flask.Response(
		'OK',
		status=200,
		mimetype='text/plain')


@app.errorhandler(500)
def unauthorized_500(error):
	return flask.Response(
		'Pretend nothing is wrong.',
		status=200,
		mimetype='text/plain')


@app.errorhandler(403)
def unauthorized_403(error):
	return flask.Response(
		'You are not authorized to access this service.',
		status=403,
		mimetype='text/plain')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3201)


