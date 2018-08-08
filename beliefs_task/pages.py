from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd
import random
import json
from common_helper_functions import task_sequence_table_info, get_expiration_time, get_video_url, Tasks, set_default_pvars

def get_beldat(page_obj):
    # Get belief rows already used
    bgid = page_obj.participant.vars["beliefs_round_data"]
    # If we've stored data for the round return it
    if page_obj.round_number == len(bgid):
        return bgid[-1]

    # Get already used gids
    used_gids = [str(bq["gid"]) for bq in bgid]
    # Get the data from the constants model
    locale = page_obj.participant.vars["locale"]
    dat = page_obj.session.vars["beliefs_" + locale + "_dat"]

    # The unique gids in the data
    unique_gids = [str(i) for i in dat["gid"].unique()]
    # Find rows that haven't been used so far
    rand_group = [str(i) for i in unique_gids if str(i) not in used_gids]

    # Select one of them at random
    #group_choice = random.choice(rand_group)

    # Select them in order
    group_choice = rand_group
    group_choice.sort()
    group_choice = group_choice[0]

    # Get the rows of the data for this random group
    group_rows = [str(i) == group_choice for i in dat["gid"]]
    group_dat = dat.loc[group_rows]

    # The unique qids in the data
    unique_gids = [str(i) for i in group_dat["qid"].unique()]
    # Select one of them at random
    row_choice = random.choice(unique_gids)

    # The data for this round
    rdat = [str(i) == row_choice for i in group_dat["qid"]]
    rdat = group_dat.loc[rdat]

    bin_labels = [str(rdat["bin" + str(b)].iloc[0]) for b in range(1, 11) if str(rdat["bin" + str(b)].iloc[0]) != "nan"]
    alt_labels = [str(rdat["alt" + str(b)].iloc[0]) for b in range(1, 11) if str(rdat["alt" + str(b)].iloc[0]) != "nan"]

    # If bin_button is empty, don't show the button to toggle alt labels
    bin_button = str(rdat["bin_button"].iloc[0]).strip()
    bin_button = bin_button if bin_button != "nan" else ""

    pay_by = str(rdat["pay_by"].iloc[0]).strip()

    beldat = {
            "qid"       : str(rdat["qid"].iloc[0]),
            "gid"       : str(rdat["gid"].iloc[0]),
            "tokens"    : int(rdat["tokens"].iloc[0]),
            "alpha"     : float(rdat["alpha"].iloc[0]),
            "delta"     : float(rdat["delta"].iloc[0]),
            "currency"  : str(rdat["currency"].iloc[0]),
            "text"      : str(rdat["text"].iloc[0]),
            "alt_text"  : str(rdat["alt_text"].iloc[0]),
            "bin_button": bin_button,
            "alt_button": str(rdat["alt_button"].iloc[0]),
            "pay_by"    : pay_by,
            "bin_labels": bin_labels,
            "alt_labels": alt_labels,
            "num_bins"  : len(bin_labels),
                }

    # Store this data in the round data
    page_obj.participant.vars["beliefs_round_data"].append(beldat)
    return(beldat)

def set_beliefs_data(page_obj):
        for p in page_obj.subsession.get_players():
            set_default_pvars(p)
            locale = p.participant.vars["locale"]
            nrounds = page_obj.session.vars["beliefs_" + locale + "_dat"]["gid"].unique()
            nrounds = len(nrounds)
            p.participant.vars["beliefs_num_rounds"] = nrounds

class Intro(Page):
    def vars_for_template(self):
        # Set the belief data for the participant
        set_beliefs_data(self)

        table_details = task_sequence_table_info(self, Constants.app_name)
        return {
            "app_sequence": table_details['sequence'],
            "apps_completed": table_details['num_tasks_completed'],
            "expiration_time": get_expiration_time(self),
        }

    def is_displayed(self):
        return self.round_number == 1

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            "expiration_time": get_expiration_time(self),
            "video_url"      : get_video_url(self.participant.vars["locale"], Tasks.beliefs),
        }

class TaskPage(Page):
    form_model  = "player"

    def initial_values(self):
        rnum = self.round_number
        # Randomize the data if we're in the first round
        if rnum == 1 and "beldat_is_set" not in self.participant.vars:
            self.participant.vars["beldat_is_set"] = True
            # Record the choices for every round here
            self.participant.vars["beliefs_choice"] = []
            # Record the data for each choice
            self.participant.vars["beliefs_round_data"] = []

    def get_form_fields(self):
        # Set initial values for this participant
        self.initial_values()
        # The belief data
        beldat = get_beldat(self)
        # Add the labelset val as wel
        form_fields = ["bin" + str(i) for i in range(1, len(beldat["bin_labels"]) + 1)] + ["labelset"] + ["timeStamps"]
        return(form_fields)

    def vars_for_template(self):
        # Set initial values for this participant
        self.initial_values()

        # The lottery data for this row
        beldat = get_beldat(self)

        # Where the session is taking place
        locale = self.participant.vars["locale"]

        # Save the qid chosen to the data
        setattr(self.player, "qid", str(beldat["qid"]))

        beliefs = {"round_number"    : self.round_number,
                   "number_of_rounds": self.participant.vars["beliefs_num_rounds"],
                   "hex_colors"      : self.session.vars["beliefs_hex_colors"],
                   "beldat"          : beldat,
                   "tokens"          : beldat["tokens"],
                   "currency"        : beldat["currency"],
                   "locale"          : locale,
                   "task_number"     : 1,
               }


        return {
            "beliefs": beliefs,
            "expiration_time": get_expiration_time(self),
            "video_url": get_video_url(self.participant.vars["locale"], Tasks.beliefs)
        }

    def is_displayed(self):
        return self.round_number <= self.participant.vars["beliefs_num_rounds"]

    def before_next_page(self):
        choice = [getattr(self.player, "bin" + str(b)) for b in range(1, 11)]
        self.participant.vars["beliefs_choice"].append(choice)

class Results(Page):
    form_model  = "player"

    def vars_for_template(self):
        # The number of rounds
        num_rounds = self.participant.vars["beliefs_num_rounds"]
        # Select a round at random for payment
        if "beliefs_pay_round" not in self.participant.vars:
            pay_round = [i for i in range(0, num_rounds)]
            pay_round = random.choice(pay_round)
            self.participant.vars["beliefs_pay_round"] = pay_round
        else:
            pay_round = self.participant.vars["beliefs_pay_round"]

        # The saved choices made by the subject
        choices_made = self.participant.vars["beliefs_choice"]
        pay_choices = choices_made[pay_round]

        # The lottery data for this row
        beldat = self.participant.vars["beliefs_round_data"][pay_round]
        # Save the qid chosen for payment
        setattr(self.player, "pay_qid", str(beldat["qid"]))

        # Where the session is taking place
        locale = self.participant.vars["locale"]

        # Not really used anywhere
        final_payment = {
                "currency" : beldat["currency"],
                "amounts": [],
                "when": [beldat["pay_by"]],
                "choices": pay_choices,
                "qid" : [beldat["qid"]],
                "gid" : [beldat["gid"]]
                }
        self.participant.vars["beliefs_final_payment"] = final_payment
        setattr(self.player, "final_payment", json.dumps(final_payment))

        beliefs_results = {
                "round_number"    : self.round_number,
                "number_of_rounds": self.participant.vars["beliefs_num_rounds"],
                "hex_colors"      : self.session.vars["beliefs_hex_colors"],
                "beldat"          : beldat,
                "tokens"          : beldat["tokens"],
                "currency"        : beldat["currency"],
                "locale"          : locale,
                "task_number"     : 6,
                "expiration_time" : get_expiration_time(self),
                "pay_round": pay_round + 1,
                "pay_choices": pay_choices,
                "final_payment" : final_payment,
               }

        # Save this data for use in the final results page
        self.participant.vars["beliefs_results"] = beliefs_results

        return {
            "beliefs" : beliefs_results,
            "expiration_time": get_expiration_time(self),
        }

    def is_displayed(self):
        return self.round_number == self.participant.vars["beliefs_num_rounds"]

class Overview(Page):
    def vars_for_template(self):
        tvars = {
                "locale": self.participant.vars["locale"],
                "expiration_time": get_expiration_time(self),
                }
        return tvars

    def is_displayed(self):
        return self.round_number == 1

page_sequence = [
    Intro,
    Instructions,
    Overview,
    TaskPage,
    Results,
]
