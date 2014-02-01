#!/usr/bin/env python

import json, authsettings, os, traceback

import flask
app = flask.Flask(__name__)

import handlers
import smartass


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


