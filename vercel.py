import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'select_class.settings')
os.environ.setdefault('PYTHON_PATH', '.')

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

application = get_wsgi_application()
application = WhiteNoise(application)

# Add static files handling
staticfiles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
if os.path.exists(staticfiles_dir):
    application.add_files(staticfiles_dir, prefix='static/')

# Init the app
app = application
