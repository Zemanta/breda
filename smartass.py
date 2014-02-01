import os, random
import logging

here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

breda_brain = None
breda_brain_path = here("../breda.brain")

try:
	from cobe.brain import Brain
	if os.path.exists(breda_brain_path):
		breda_brain = Brain(breda_brain_path)
except Exception, e:
	logging.info('Brains not loaded %s', repr(e))


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

def smartreplay(message):
	return breda_brain.reply(' '.join(message[1:]))

def replay(message):
	if breda_brain:
		return smartreplay(message)
	return randomretort(message)
