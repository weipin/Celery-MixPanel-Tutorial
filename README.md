Celery-MixPanel-Tutorial is a simple Python script to send data to [MixPanel](https://mixpanel.com/) asynchronously. It uses [Celery](http://www.celeryproject.org/) as queue system and [Eventlet](http://eventlet.net/) for concurrent networking. While being standalone, the project works well with Django as a Django app.

As the name suggests, the project serves as a step-by-step tutorial to Celery beginner.


Notice
====
- This project isn't affiliated with the Mixpanel company.
- Error checking is completely ignored.
- The installation/setup tutorial is rough.
- There aren't many lines of code, please use until you've reviewed it.

Problem
====
You need to send data from your backend to MixPanel, in an asynchronously way. The [official sample script](https://mixpanel.com/docs/integration-libraries/python) works but consumes too much resources for a busy backend.

Solution
====
With [Celery](http://celeryproject.org/), an asynchronous task queue/job queue, we can execute tasks concurrently. Further more, by employing [Eventlet](http://eventlet.net/), a concurrent networking library for Python, performance can be greatly improved.

Installation and Setup
====

Install Celery.
```
pip install Celery
```

Install Eventlet and the dnspython module.
```
pip install eventlet
pip install dnspython
```

Celery requires a separate service called a [message broker](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#choosing-a-broker). While the default broker is [RabbitMQ](http://www.rabbitmq.com/), this tutorial uses [Redis](http://redis.io/) as an alternative.
```
sudo apt-get install redis-server
```

And the Python dependencies:
```
pip install -U celery-with-redis
```

To use this script with Django (optional), you need django-celery.
```
pip install django-celery
```

Filling your MixPanel API token
====
Find celeryconfig.py in mixpanel folder and replace the value of MIXPANEL_API_TOKEN with yours.

```
MIXPANEL_API_TOKEN = 'xxxxx'
```

Starting worker
====
After installing the necessary components, we can start the worker process. 
```
cd mixpanel
celery worker -l info --concurrency=100 --pool=eventlet
```

Notes:

- The worker process is started using the celery worker manage command for convenience. To run the worker as a daemon, please see the section "Running worker as daemon" below.
- We specifies Eventlet as the execution pool implementation (`--pool=eventlet`). In the cases that networking is the only thing a task do, Eventlet can be used to efficiently spawn hundreds of green threads.
- We specifies the number of concurrent worker as 100 (`--concurrency=100`).
- `celery` will find the default config file `celeryconfig.py` and then the task in `tasks.py`.


Calling the task
=====
With the worker waiting for tasks, we can now issue one. Open a new terminal session, in the folder which contains the mixpanel folder, start the Python interpreter and execute:
```
import celery
from mixpanel import tasks
from mixpanel import celeryconfig

c = celery.app.default_app
c.config_from_object(celeryconfig)

tasks.track.delay('test_event')
```

- The delay() method is a shortcut to the apply_async() method, which controls the task execution.

- If all goes well, you should see a positive result like:
```
<AsyncResult: a783338b-818d-46f0-bf4b-c7811abda7e2>
```

- In the worker's session, you should see a positive log as well:
```
[2013-06-02 09:34:28,289: INFO/MainProcess] Task mixpanel.tasks.track[a783338b-818d-46f0-bf4b-c7811abda7e2] succeeded in 0.705556869507s: None
```

- In MixPanel, a new event 'test_event' should appear.

- Unlike starting the worker, here we have to load the configuration for the Celery application manually.


Working with Django
====
Copy the mixpanel folder to your Django project as an app. In settings.py, add djcelery and mixpanel to INSTALLED_APPS, and add the following lines (replace MIXPANEL_API_TOKEN with yours):
```
MIXPANEL_API_TOKEN = 'xxxxxxxxx'

BROKER_URL = 'redis://localhost:6379/0'

import djcelery
djcelery.setup_loader()
```

To start worker:
```
./manage.py celery worker -l info --concurrency=100  --pool=eventlet
```

To call the task:
```
./manage.py shell

>>> from mixpanel import tasks
>>> tasks.track.delay('test_event')

```

Running worker as daemon
====

To run the worker in the background as a daemon, see the official doc [Running the worker as a daemon](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#daemonizing) for more information. In the extra folder, you can find two supervisord configure files as a starting point, one for Python, the other for Django.


Notes
====

- Starting worker and calling task is separate, meaning you can start the worker with Django but call the task "directly", and vice versa.

- Using default Celery application [is not encouraged](http://docs.celeryproject.org/en/latest/userguide/application.html#laziness). Celery-MixPanel-Tutorial uses the default Celery application to make the task work with Django, which is how it seems to work.
