#-*- coding: utf-8 -*-

import urllib2, time, re, random, json

def _pic(url, title=None):
	if '?' in url:
		concat_char = '&'
	else:
		concat_char = '?'
	if title:
		return '<%s%scb=%s.jpg|%s>' % (url, concat_char, time.time(), title)
	else:
		return '<%s%scb=%s.jpg>' % (url, concat_char, time.time())

def piramida(user, chan, message):
	menu = urllib2.urlopen('http://pizzerijapiramida.si/malice/').read()
	ts = time.localtime()
	tss = ', %s.%s.%s' % (ts.tm_mday, ts.tm_mon, ts.tm_year % 100)
	start = menu.find(tss) + len(tss)
	end = menu.find('</div>', start)
	daymenu = re.sub(r'<[^>]+?>', ' ', menu[start:end])
	daymenu = daymenu.replace('\n', '').replace('\r', '').replace('€', '€\n').replace('&nbsp;', '')
	daymenu = re.sub(r' +', ' ', daymenu)
	daymenu = daymenu.replace(' 1.', '\n 1.')
	if len(daymenu) > 20:
		return tss[2:] + '\n' + daymenu
	else:
		return "I really can't tell, head to <http://pizzerijapiramida.si/malice/|the page> to see what's cookin'."

def radar(u, c, m):
	return _pic('http://www.arso.gov.si/vreme/napovedi%20in%20podatki/radar_anim.gif', 'SIRAD')

def where(u, c, m):
	return '<https://github.com/Zemanta/breda|At home, of course.>'

def bicikelj(u, c, m):
	return "They were all stolen, so just take a hike."

def wat(u, c, m):
	wat = json.load(urllib2.urlopen('http://watme.herokuapp.com/random')).get('wat')
	if wat:
		return _pic(wat)
	else:
		return _pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif')
	
def isee(u, c, m):
	return _pic('http://bukk.it/fry-see.gif', 'isee')
	
def mijau(u, c, m):
	url='http://thecatapi.com/api/images/get?format=src&type=gif'
	return '<%s>' % urllib2.urlopen(urllib2.Request(url)).geturl()

def meow(u, c, m):
	return mijau(u, c, m)

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		if sys.argv[1] in vars().keys():
			print vars()[sys.argv[1]](None, None, None)
	else:
		for k in locals().keys():
			if k.startswith('_'):
				continue
			if hasattr(locals()[k], '__module__') and locals()[k].__module__ == '__main__':
				print k
