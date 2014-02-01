#!/usr/bin/env python

import sys, json, authsettings, random, os, traceback

import flask
app = flask.Flask(__name__)

import handlers

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

try:
	from cobe.brain import Brain
	breda_brain_path = here("../breda.brain")
	if os.path.exists(breda_brain_path):
		breda_brain = Brain(breda_brain_path)
	else:
		raise Exception('No brain file found')
except Exception:
	breda_brain = None


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

def cobe_replay(message):
	return breda_brain.replay(message)

@app.route('/msg/', methods=['POST'])
def process_message():
	if flask.request.form.get('token') != authsettings.AUTH_TOKEN:
		flask.abort(403)
	user = flask.request.form.get('user_name')
	chan = flask.request.form.get('channel_name')
	message = flask.request.form.get('text').split()
	try:
		if hasattr(handlers, message[1].lower()):
			return json.dumps(dict(text=getattr(handlers, message[1].lower())(user, chan, message)))
		elif breda_brain:
			return json.dumps(dict(text=cobe_replay(message)))
		else:
			return json.dumps(dict(text=randomretort(message)))
	except:
		return json.dumps(dict(text="Oh, bummer: " + traceback.format_exc()))

@app.route('/push/', methods=['POST'])
def push():
	data = json.loads(flask.request.form.get('payload', {}))
	if not data:
		return ''
	os.system('git pull')
	return 'OK'

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
	app.run(host='0.0.0.0', port=3201, debug=('debug' in sys.argv))


