# -*- coding: utf-8 -*-
import datetime
import urllib2
import time
import re
import json
import random
import traceback
from urlparse import parse_qs
from bs4 import BeautifulSoup


def flask_handler():
    user = request.form.get('user_name')
    chan = request.form.get('channel_name')
    chunks = request.form.get('text').encode('utf-8').split()
    return json.dumps(slack(user, chan, chunks))


def lambda_handler(event, context):
    req_body = event['body']
    params = parse_qs(req_body)
    user = params['user_name'][0]
    chan = params['channel_name'][0]
    chunks = params['text'][0].encode('utf-8').split()
    return slack(user, chan, chunks)


def slack(user, chan, chunks):
    if len(chunks) >= 2:
        command = chunks[1]
    else:  # no command
        return json.dumps(dict(text='What is it?'))
    g = globals()
    if 'slack_' + command in g:
        return dict(text=g['slack_' + command](user, chan, chunks))
    else:
        return dict(text="I don't know about %s." % command)


def _pic(url, title=None):
    if '?' in url:
        concat_char = '&'
    else:
        concat_char = '?'
    if title:
        return '<%s%scb=%s.jpg|%s>' % (url, concat_char, time.time(), title)
    else:
        return '<%s%scb=%s.jpg>' % (url, concat_char, time.time())
    

def slack_decide(user, chan, chunks):
    return random.choice(chunks[2:])


def slack_bicikelj(u, c, m):
    station_name = ' '.join(m[2:])
    if not station_name:
        station_name = 'TIVOLI'
    try:
        f = urllib2.urlopen('http://prevoz.org/api/bicikelj/list/')
        d = f.read()
        j = json.loads(d)

        last_update = int(time.time() - int(j['updated']))

        if station_name == 'LIST':
            station_names = []
            for station in j['markers'].itervalues():
                station_names.append(station['name'])
            return "List of stations: %s" % ", ".join(station_names)
        elif station_name == 'ALL':
            retstr = "All stations (updated %s seconds ago):\n" % last_update
            for station in j['markers'].itervalues():
                retstr += "%s: %s bikes / %s spaces\n" % (station['name'], station['station'][
                                                          'available'], station['station']['free'])
            return retstr
        else:
            my_station_id = None
            for station_id, station in j['markers'].iteritems():
                if station['name'] == station_name:
                    my_station_id = station_id
            if my_station_id is None:
                return "Bicikelj station '%s' not found - try 'TIVOLI' or something..." % station_name
            else:
                station = j['markers'][my_station_id]
                return "Bicikelj data for %s: %s bikes / %s spaces (updated %s seconds ago)" % (station['name'], station['station']['available'], station['station']['free'], last_update)
    except:
        return "Uh, I can't... Seems there's an error, hope you can make sense of it: " + traceback.format_exc()


def slack_makin(u, c, m):
    if m[2] != 'copies':
        return
    name = ' '.join(m[3:])
    endings = [
        'ski',
        'inator',
        'tholmeau',
        'as',
        'kadaka',
        'chop',
        'erino',
        name[-1:] + name[-1:] + name[-1:] + name[-1:],
        'wise',
        'man',
        'atollah',
        'ster',
        'ino',
        'ipulator',
        'meister',
    ]
    rand1 = random.choice(endings)
    rand2 = random.choice(endings)
    return "%s%s! the %s%s!" % (name, rand1, name, rand2)


def slack_piramida(user, chan, message):
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
        ret = tss[2:] + '\n' + daymenu
        return ret.decode('utf-8')
    else:
        return "I really can't tell, head to <http://pizzerijapiramida.si/malice/|the page> to see what's cookin'."


def slack_pivnica(user, chan, message):
    site = BeautifulSoup(urllib2.urlopen('http://www.pivnica-union.si/si/').read(), "html.parser")
    for day_title in site.find_all('h4', class_='foodDayMenuBlockTitle'):
        if time.strftime('%-d. %-m.') in day_title.string:
            return "\n".join(day_title.find_next('div', class_='foodItemDesc').stripped_strings)
    return "I really can't tell, head to <http://www.pivnica-union.si/si/> to see what's cookin'."


def slack_dishi(user, chan, message):
    site = BeautifulSoup(urllib2.urlopen(
        'http://www.gostilne.si/jedilnik.php?uid=910').read(), "html.parser")
    items = site.find_all('div', class_='menu')
    if items:
        return "\n".join(item.get_text() for item in items)
    return "I really can't tell, head to <http://dishi.eu/?page_id=28> to see what's cookin'."


def slack_chinese(user, chan, message):
    site = BeautifulSoup(urllib2.urlopen('http://www.dobrotevzhoda.si/jedilni-list/').read(), 'html.parser')
    items = site.find_all('h2', class_='tabtitle')
    for h2 in items:
        if h2.text == 'KOSILO':
            break
    else:
        return "I really can't tell, head to <http://www.dobrotevzhoda.si/jedilni-list/> to see what's cookin'."

    for next_element in h2.next_elements:
        if next_element.name == 'table':
            break
    else:
        return "I really can't tell, head to <http://www.dobrotevzhoda.si/jedilni-list/> to see what's cookin'."

    days = {
        1: 'Ponedeljek',
        2: 'Torek',
        3: 'Sreda',
        4: u'Četrtek',
        5: 'Petek',
        6: 'Sobota',
        7: 'Nedelje',
    }
    found_day = False
    lst = []
    today_str = days[datetime.date.today().isoweekday()]
    for tr in next_element.find_all('tr'):
        if not found_day and today_str not in tr.text:
            continue

        found_day = True
        if today_str not in tr.text and any(day in tr.text for day in days.values()):
            break

        lst.append(' '.join(e.text for e in tr.find_all('td')))
    return '\n'.join(lst)


def slack_food(user, chan, message):
    list = [
        "*Piramida*\n%s" % slack_piramida(user, chan, message),
        "*Pivnica*\n%s" % slack_pivnica(user, chan, message),
        "*Dishi*\n%s" % slack_dishi(user, chan, message)
    ]
    return "\n\n".join(list)


def slack_radar(u, c, m):
    return _pic('http://www.arso.gov.si/vreme/napovedi%20in%20podatki/radar_anim.gif', 'SIRAD')


def slack_where(u, c, m):
    return '<https://github.com/idioterna/breda|At home, of course.>'


def slack_wat(u, c, m):
    wat = json.load(urllib2.urlopen('http://watme.herokuapp.com/random')).get('wat')
    if wat:
        return _pic(wat)
    else:
        return _pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif')


def slack_random(u, c, m):
    data = json.load(urllib2.urlopen(
        'http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC')).get('data', {}).get('image_url')
    if data:
        return _pic(data)
    else:
        return _pic('http://www.babel.crackerboxpalace.com/gifs/strangelove-wat.gif')


if __name__ == '__main__':
    from flask import Flask, request
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.add_url_rule('/slack/', 'slack', flask_handler, methods=['POST'])
    app.run()
