#!/usr/bin/env python

import sys, json, authsettings, random, os
import flask
app = flask.Flask(__name__)

import handlers

def randomretort(message):
	retorts = [
		"I don't have a clue about %s!",
		"Never heard of it!",
		"Dunno",
		"No idea.",
		"Haven't the faintest.",
		"Should %s mean anything to me?",
		"%s? That place in Hungary?",
		"Did you mean <http://google.com/?q=beaver+tails|Beaver Tails>?",
	]
	ret = random.choice(retorts)
	if '%s' in ret:
		return ret % ' '.join(message[1:])
	else:
		return ret

@app.route('/msg/', methods=['POST'])
def process_message():
	if flask.request.form.get('token') != authsettings.AUTH_TOKEN:
		flask.abort(403)
	user = flask.request.form.get('user_name')
	chan = flask.request.form.get('channel_name')
	message = flask.request.form.get('text').split()
	if hasattr(handlers, message[1].lower()):
		return json.dumps(dict(text=getattr(handlers, message[1].lower())(user, chan, message)))
	else:
		return json.dumps(dict(text=randomretort(message)))
	print json.dumps(flask.request.form, indent=2)
	return '{}'

@app.route('/push/', methods=['POST'])
def push():
	data = json.loads(flask.request.form.get('payload', {}))
	if not data:
		return ''
	os.system('git pull')
	return 'OK'

@app.errorhandler(500)
def unauthorized(error):
	return flask.Response(
		'Pretend nothing is wrong.',
		status=200,
		mimetype='text/plain')

@app.errorhandler(403)
def unauthorized(error):
	return flask.Response(
		'You are not authorized to access this service.',
		status=403,
		mimetype='text/plain')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3201, debug=('debug' in sys.argv))


