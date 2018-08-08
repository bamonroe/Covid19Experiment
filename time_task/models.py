from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# To read from the CSV file
import pandas as pd

from common_helper_functions import set_default_pvars

author = 'Brian Albert Monroe'

doc = """
A discounting task
"""

def get_block_names(dat):
    return(dat["block_id"].unique())

class Constants(BaseConstants):
    num_rounds = 30
    name_in_url = 'task_t'
    players_per_group = None
    app_name = 'time_task'

class Subsession(BaseSubsession):
    def creating_session(self):
        ## DEBUG
        for p in self.get_players():
            set_default_pvars(p)

        num_per_page = 5

        for locale in ["usa", "rsa"]:
            dat = pd.read_csv("configs/time_input_" + locale + ".csv")
            self.session.vars[locale + "_time_dat"] = dat

        # Colors picked with a good pallete
        # They overwrite, so just put the one you want here
        time_hex_colors = ["#F8766D", "#00BA38", "#619CFF"]

        for p in self.get_players():
            locale      = p.participant.vars["locale"]
            dat         = self.session.vars[locale + "_time_dat"]
            block_names = get_block_names(dat)

            # Show a maximum of 20 groups if more than 20 are set
            num_rounds = min(len(block_names), 20)

            p.participant.vars["time_hex_colors"] = time_hex_colors
            p.participant.vars["time_num_rounds"] = num_rounds
            p.participant.vars["time_block_names"] = block_names
            p.participant.vars["time_num_per_page"] = num_per_page

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    choice_for_payment = models.StringField()
    block_for_payment  = models.StringField()
    final_payment = models.StringField()

    block_ID    = models.StringField()

    choice_1    = models.IntegerField()
    pair_ID_1   = models.StringField()

    choice_2    = models.IntegerField()
    pair_ID_2   = models.StringField()

    choice_3    = models.IntegerField()
    pair_ID_3   = models.StringField()

    choice_4    = models.IntegerField()
    pair_ID_4   = models.StringField()

    choice_5    = models.IntegerField()
    pair_ID_5   = models.StringField()

    timeStamps  = models.StringField()
