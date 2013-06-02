import os
import sys
sys.path.insert(0, os.path.dirname(os.getcwd()))

MIXPANEL_API_TOKEN = 'xxxxx'

BROKER_URL = 'redis://localhost:6379/0'

CELERY_IMPORTS = ('mixpanel.tasks')

