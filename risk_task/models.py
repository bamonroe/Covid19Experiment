from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# To read from the CSV file
import pandas as pd
# To ranomize the rows
import random

def getAvals(row):
    ocounter = 0
    while True:
        try:
            tmp = row["A" + str(ocounter)]
            ocounter = ocounter + 1
        except:
            ocounter = ocounter - 1
            break
    return ocounter

author = 'Brian Albert Monroe'

doc = """
A risk task
"""

def get_pvar(p, var):
    pvar = p.participant.vars
    defaults = {
            "locale": "usa",
            }
    if var in pvar:
        return pvar[var]
    else:
        if var in defaults:
            print("WARNING: You're using a default value for a participant.var, not one that was found")
            p.participant.vars[var] = defaults[var]
            return defaults[var]
        else:
            raise Exception("The variable '" + var + "' isn't in the participant.vars and doesn't have a default defined.")

class Constants(BaseConstants):
    # Hard-coded to allow less than this number of lottery pairs
    num_rounds = 100
    name_in_url = 'task_r'
    players_per_group = None
    app_name = 'risk_task'

class Subsession(BaseSubsession):
    def creating_session(self):

        for locale in ["usa", "rsa"]:
            dat = pd.read_csv("configs/risk_input_" + locale + ".csv")
            self.session.vars[locale + "_risk_dat"] = dat

        for p in self.get_players():
            if "risk_dat" not in p.participant.vars:

                locale = get_pvar(p, "locale")
                dat = self.session.vars[locale + "_risk_dat"]

                risk_num_ops = getAvals(dat.iloc[0, :])
                p.participant.vars["risk_num_rounds"] = len(dat["luid"])

                if risk_num_ops + 1 == 2:
                    risk_hex_colors = ["#F8766D", "#00BFC4"]
                elif risk_num_ops + 1 == 3:
                    risk_hex_colors = ["#F8766D", "#00BA38", "#619CFF"]
                elif risk_num_ops + 1 == 4:
                    risk_hex_colors = ["#F8766D", "#7CAE00", "#00BFC4", "#C77CFF"]
                elif risk_num_ops + 1 == 5:
                    risk_hex_colors = ["#F8766D", "#A3A500", "#00BF7D", "#00B0F6" "#E76BF3"]
                else:
                    risk_hex_colors = ["#F8766D", "#A3A500", "#00BF7D", "#00B0F6" "#E76BF3"]

                p.participant.vars["risk_num_ops"]    = risk_num_ops
                p.participant.vars["risk_hex_colors"] = risk_hex_colors

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    choice_for_payment = models.IntegerField()
    pair_for_payment   = models.IntegerField()
    roll_for_payment   = models.IntegerField()

    final_payment      = models.StringField()

    choice             = models.IntegerField()
    lot_id             = models.StringField()
    timeStamps         = models.StringField()
