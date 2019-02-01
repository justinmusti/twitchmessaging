import os


APP_STAGE = os.environ.get('APP_STAGE', 'development')

if APP_STAGE == 'production':
    from .production import *
elif APP_STAGE in ['development']:
    from .development import *
elif APP_STAGE == 'staging':
    from .staging import *

else:
    raise Exception('Unexpected APP_STAGE environment.')
