from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from common_helper_functions import set_default_pvars

# To read from the CSV file
import pandas as pd

author = 'Brian Albert Monroe'

doc = """
A discounting task
"""

def getAvals(row):
    ocounter = 0
    while True:
        try:
            tmp = row["p" + str(ocounter) + "_events"]
            ocounter = ocounter + 1
        except:
            ocounter = ocounter - 1
            break
    return ocounter

class Constants(BaseConstants):
    num_rounds = 45
    name_in_url = 'task_ca'
    players_per_group = None
    app_name = 'ca_task'

class Subsession(BaseSubsession):
    def creating_session(self):
        # DEBUG
        for p in self.get_players():
            set_default_pvars(p)

        for locale in ["usa", "rsa"]:
            dat = pd.read_csv("configs/ca_input_" + locale + ".csv")
            self.session.vars[locale + "_ca_dat"] = dat

        for p in self.get_players():

            locale =  p.participant.vars["locale"]
            dat = self.session.vars[locale + "_ca_dat"]

            p.participant.vars["ca_num_ops"]    = getAvals(dat.iloc[0, :])
            p.participant.vars["ca_num_rounds"] = len(dat["pair_id"])
            p.participant.vars["ca_hex_colors"] = ["#F8766D", "#00BFC4"]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    choice_for_payment = models.IntegerField()

    final_payment = models.StringField()

    top_option = models.StringField()

    choice  = models.StringField()
    pair_ID = models.StringField()

    timeStamps  = models.StringField()
