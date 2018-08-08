from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)

author = 'Brian Albert Monroe'

doc = """
Beliefs Task
"""
# To read from the CSV file
import pandas as pd

class Constants(BaseConstants):
    name_in_url = 'beliefs'
    num_rounds = 10
    players_per_group = None
    app_name = 'beliefs_task'

    # Colors picked with a good pallete
    hex_colors = ["#F8766D", "#00BFC4"]
    hex_colors = ["#F8766D", "#00BA38", "#619CFF"]
    hex_colors = ["#F8766D", "#7CAE00", "#00BFC4", "#C77CFF"]
    hex_colors = ["#F8766D", "#A3A500", "#00BF7D", "#00B0F6" "#E76BF3"]
    hex_colors = ["#F8766D", "#A3A500", "#00BF7D", "#00B0F6" "#E76BF3"]

class Subsession(BaseSubsession):
    def creating_session(self):
        usa_dat = pd.read_csv("configs/beliefs_input_usa.csv")
        rsa_dat = pd.read_csv("configs/beliefs_input_rsa.csv")

        self.session.vars["beliefs_usa_dat"] = usa_dat
        self.session.vars["beliefs_rsa_dat"] = rsa_dat
        self.session.vars["beliefs_hex_colors"] = ["#F8766D", "#A3A500", "#00BF7D", "#00B0F6" "#E76BF3"]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    qid         = models.StringField()
    labelset    = models.IntegerField(default = 0)
    pay_qid     = models.StringField()

    final_payment = models.StringField()

    bin1  = models.IntegerField(default = 0)
    bin2  = models.IntegerField(default = 0)
    bin3  = models.IntegerField(default = 0)
    bin4  = models.IntegerField(default = 0)
    bin5  = models.IntegerField(default = 0)
    bin6  = models.IntegerField(default = 0)
    bin7  = models.IntegerField(default = 0)
    bin8  = models.IntegerField(default = 0)
    bin9  = models.IntegerField(default = 0)
    bin10 = models.IntegerField(default = 0)

    timeStamps = models.StringField()
