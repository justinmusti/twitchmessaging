import os

APP_STAGE = os.environ.get('APP_STAGE', 'development')

if APP_STAGE == 'production':
    from .production import *
elif APP_STAGE in ['development', 'staging']:
    from .development import *
else:
    raise Exception('Unexpected APP_STAGE environment.')
