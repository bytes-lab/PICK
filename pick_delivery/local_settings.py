# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "eac*+7=6p-lk*n#mx(ro8%z(90kjw*#z^i86$w5ebv581kajqoze"
NEVERCACHE_KEY = "wwvuoe^l(bj^2gz1@^_wugomcjb32pyjr@nfg!a@#tj$in!)wl"

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS = ["api.pick.sa"]
# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

FABRIC = {
    "DEPLOY_TOOL": "git",  # Deploy with "git", "hg", or "rsync"
    "SSH_USER": "root",  # VPS SSH username
    "SSH_PASS":  '@5pick;', # SSH password (consider key-based authentication)    
    "VIRTUALENV_HOME":  "/home/root/do", # Absolute remote path for virtualenvs
    "PROJECT_NAME": "pick_delivery", # Unique identifier for project
    "GUNICORN_PORT": 8000, # Port gunicorn will listen on
    "REPO_URL": "https://github.com/jason5001001/pick_delivery.git", # Git or Mercurial remote repo URL for the project
    "HOSTS": ["159.203.47.245"],  # The IP address of your VPS
    "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
    "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
    "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
    "DB_PASS": "pickswift@123",  # Live database password
    "ADMIN_PASS": "pickswift@123",  # Live admin user password
    "SECRET_KEY": SECRET_KEY,
    "NEVERCACHE_KEY": NEVERCACHE_KEY,
}
