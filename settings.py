from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'prisoner',
        'display_name': "Infinitely Repeated Prisoner's Dilemma (1 Group, 1 Match)",
        'num_demo_participants': 2,
        'app_sequence': ['prisoner'],
    },
]
# see the end of this file for the inactive session configs


SESSION_FIELDS = [
    'start_time',
    'alive'
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True

ROOMS = [
    dict(
        name='live_demo',
        display_name='Room for Live Demo (No Participant Labels)',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
tmp_SECRET_KEY = '123456789'
SECRET_KEY = tmp_SECRET_KEY

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
