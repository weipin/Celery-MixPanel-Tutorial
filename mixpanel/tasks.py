import base64
import json

from eventlet.green import urllib2
from celery import task

try:
    import celeryconfig
    token = celeryconfig.MIXPANEL_API_TOKEN
except:
    from django.conf import settings
    token = settings.MIXPANEL_API_TOKEN

@task(ignore_result=True)
def track(event, properties=None):
    if properties is None:
        properties = {}
    
    if 'token' not in properties:
        properties['token'] = token

    params = {'event': event, 'properties': properties}
    data = base64.b64encode(json.dumps(params))
    url = 'http://api.mixpanel.com/track/?data=' + data
    urllib2.urlopen(url)

