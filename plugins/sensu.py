'''!stash [client-name] [reason]'''
import urllib2
import json
import os
import time
import re

DEFAULT_EXPIRE = int(os.getenv('SENSU_STASH_EXPIRE', 3600*24))    # 24 hr, unit: seconds
SENSU_API_BASE_URL = os.getenv('SENSU_API_BASE_URL', 'http://sensu.vkportal.com:4567')
STASHES_URL = '{}/stashes'.format(SENSU_API_BASE_URL)
CLIENTS_URL = '{}/clients'.format(SENSU_API_BASE_URL)

SOURCE = os.getenv('SENSU_STASH_SOURCE', 'slack')


def createStash(msg):
    # msg should be "!stash <name> <reason>"
    pieces = msg.split(' ', 2)
    if len(pieces) != 3:
        return ''

    name = pieces[1]
    reason = pieces[2]

    if not clientExists(name):
        return 'Could not find a client named {}'.format(name)

    payload = createPayload(name, reason)

    urllib2.urlopen(STASHES_URL, json.dumps(payload))
    return 'Stash created!'


def clientExists(name):
    res = urllib2.urlopen(CLIENTS_URL)
    body = res.read()
    j = json.loads(body)
    return len([x for x in j if x['name'] == name]) == 1


def createPayload(name, reason):
    return {
        'path': 'silence/{}'.format(name),
        'expire': DEFAULT_EXPIRE,
        'content': {
            'reason': reason,
            'source': SOURCE,
            'timestamp': int(time.time())
        }
    }

def on_message(msg, server):
    test = msg.get('test', '')
    match = re.findall(r'!stash( .*)+', text)
    if not match: return

    return createStash(msg)
