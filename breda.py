#!/usr/bin/env python

import sys
from flask import Flask
app = Flask(__name__)

@app.route('/incoming')
def process_message():
	print repr(request)
	return '{}'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3201, debug=('debug' in sys.argv))


