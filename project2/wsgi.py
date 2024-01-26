# project2/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from mongoengine import connect

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')

# MongoDB bağlantısı
connect(
    db='migsil2',
    host='localhost',
    port=27017,
    username='Admin',
    password='erenuzun01',
    authentication_source='admin',
    tz_aware=True
)
application = get_wsgi_application()