breda
=====

Breda is a Tree

Custom commands
---------------

	Create a function in heandlers.py with a name you want breda to respond to.

Build Breda's brain
-----------------

If cobe package is installed and breda.brain database is present, Breda will use markov chain to respond to unknown queries.

	pip install cobe

	cobe learn path_to_file.txt
	// rename cobe.brain to breda.brain and copy it to the parent directory of breda
