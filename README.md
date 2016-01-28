breda
=====

Breda is a Tree

Custom commands
---------------

Create a function in main.py with a `slack_<name>` you want breda to respond to.


Build Breda's brain
-----------------

If cobe package is installed and breda.brain database is present, Breda will use markov chain to respond to unknown queries.

	pip install cobe

	cobe learn path_to_file.txt
	// rename cobe.brain to breda.brain and copy it to the parent directory of breda


Deployment
----------
Can be deployed both as a Flask app or on AWS Lambda via AWS API Gateway. When setting up the API gateway, set up a mapping template for the x-www-form-urlencoded content type with the following: `{ "body": $input.json("$") }`.
