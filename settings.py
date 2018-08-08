from os import environ
import os.path

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
        'name': 'risk_task',
        'display_name': "Risk Task",
        'num_demo_participants': 2,
        'app_sequence': ['risk_task'],
        'short_lot': False,
    },
    {
        'name': 'time_task',
        'display_name': "Time Task",
        'num_demo_participants': 2,
        'app_sequence': ['time_task'],
    },
    {
        'name': 'ca_task',
        'display_name': "Correlation Aversion Task",
        'num_demo_participants': 2,
        'app_sequence': ['ca_task'],
    },
    {
        'name': 'Beliefs',
        'display_name': "Beliefs Task",
        'num_demo_participants': 1,
        'app_sequence': ['beliefs_task'],
    },
    {
        'name': 'demog_survey',
        'display_name': "Demographics survey (default location)",
        'num_demo_participants': 5,
        'app_sequence': ['demog_survey_task'],
    },
    {
        'name': 'hsrc_survey',
        'display_name': "HSRC survey (default location)",
        'num_demo_participants': 5,
        'app_sequence': ['hsrc_survey_task'],
    },
    {
        'name': 'w1t1',
        'display_name': "w1t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 1,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w1t2',
        'display_name': "w1t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 1,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w2t1',
        'display_name': "w2t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 2,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w2t2',
        'display_name': "w2t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 2,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w3t1',
        'display_name': "w3t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 3,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w3t2',
        'display_name': "w3t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 3,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w4t1',
        'display_name': "w4t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 4,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w4t2',
        'display_name': "w4t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 4,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w5t1',
        'display_name': "w5t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 5,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w5t2',
        'display_name': "w5t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 5,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w6t1',
        'display_name': "w6t1",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 1,
        'wave': 6,
        'app_sequence': ['intro', 'demog_survey_task', 'beliefs_task', 'hsrc_survey_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
    {
        'name': 'w6t2',
        'display_name': "w6t2",
        'num_demo_participants': 5,
        'participant_time_limit_in_seconds': 150,
        'treatment': 2,
        'wave': 6,
        'app_sequence': ['intro', 'demog_survey_task', 'hsrc_survey_task', 'beliefs_task', 'risk_task', 'time_task', 'ca_task', 'final_page'],
    },
]

# This allows survey responses to be randomly filled.
# You must also make the appropriate setting in each survey page class definition
APPS_DEBUG = True

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'ZAR'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
USE_POINTS = False

ROOMS = [
        {
        'name' : 'w1t1',
        'display_name': 'Covid Experiment Wave 1 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w1t1.txt"),
        },
        {
        'name' : 'w1t2',
        'display_name': 'Covid Experiment Wave 1 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w1t2.txt"),
        },
        {
        'name' : 'w2t1',
        'display_name': 'Covid Experiment Wave 2 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w2t1.txt"),
        },
        {
        'name' : 'w2t2',
        'display_name': 'Covid Experiment Wave 2 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w2t2.txt"),
        },
        {
        'name' : 'w3t1',
        'display_name': 'Covid Experiment Wave 3 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w3t1.txt"),
        },
        {
        'name' : 'w3t2',
        'display_name': 'Covid Experiment Wave 3 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w3t2.txt"),
        },
        {
        'name' : 'w4t1',
        'display_name': 'Covid Experiment Wave 4 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w4t1.txt"),
        },
        {
        'name' : 'w4t2',
        'display_name': 'Covid Experiment Wave 4 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w4t2.txt"),
        },
        {
        'name' : 'w5t1',
        'display_name': 'Covid Experiment Wave 5 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w5t1.txt"),
        },
        {
        'name' : 'w5t2',
        'display_name': 'Covid Experiment Wave 5 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w5t2.txt"),
        },
        {
        'name' : 'w6t1',
        'display_name': 'Covid Experiment Wave 6 Treatment 1',
        'participant_label_file': os.path.join("_rooms", "w6t1.txt"),
        },
        {
        'name' : 'w6t2',
        'display_name': 'Covid Experiment Wave 6 Treatment 2',
        'participant_label_file': os.path.join("_rooms", "w6t2.txt"),
        },
    ]


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'cearruben'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '+f^j0w%srm2rfm5hq!$pxi(rkxm_k56gxs@kkm10bb_&rwp=&_'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'otreeutils']
