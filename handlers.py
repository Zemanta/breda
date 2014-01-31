#-*- coding: utf-8 -*-

import urllib2, time, re, random

def _pic(url, title='pic'):
	return '<%s?cb=%s|%s>' % (url, time.time(), title)

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
	return pic('http://www.arso.gov.si/vreme/napovedi%20in%20podatki/radar_anim.gif', 'SIRAD')

def where(u, c, m):
	return '<https://github.com/Zemanta/breda|At home, of course.>'

def bicikelj(u, c, m):
	return "They were all stolen, so just take a hike."

def wat(u, c, m):
	return pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif', 'wat')

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
