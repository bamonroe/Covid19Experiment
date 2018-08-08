from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# To read from the CSV file
import pandas as pd
from common_helper_functions import set_default_pvars

author = 'Brian Albert Monroe'

doc = """
A Final Page for Paymen
"""

class Constants(BaseConstants):
    # Hard-coded to allow less than this number of lottery pairs
    num_rounds = 1
    name_in_url = 'final'
    players_per_group = None

class Subsession(BaseSubsession):
    def creating_subsession(self):
        for p in self.get_players():
            set_default_pvars(p)

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    seen        = models.IntegerField()
    final_pay   = models.StringField()
    finish_time = models.StringField()
