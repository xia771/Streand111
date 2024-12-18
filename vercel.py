import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'select_class.settings')
os.environ.setdefault('PYTHON_PATH', '.')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Init the app
app = application
