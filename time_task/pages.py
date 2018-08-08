from ._builtin import Page, WaitPage
import pandas as pd
import random
import json
from .models import Constants
from common_helper_functions import task_sequence_table_info, get_expiration_time, get_video_url, Tasks
from datetime import datetime
from dateutil import tz

def get_pairdat(page_obj, block_to_use):
    # Get the data from the constants model
    locale = page_obj.participant.vars["locale"]
    dat    = page_obj.session.vars[locale + "_time_dat"]
    # Get the number of rows per page from the constants model
    num_per_page = page_obj.participant.vars["time_num_per_page"]
    # Get the data from the block we've selected
    gdat = dat.loc[dat["block_id"] == block_to_use]
    # Get a random sample of rows (without replacement) from this block
    rows = [i for i in range(0, len(gdat.index))]
    rows = random.sample(rows, k = num_per_page)
    rows.sort()
    # Get these actual rows
    grows = gdat.iloc[rows]

    pair_dat = {}
    for i in range(0, num_per_page):
        pair_dat[str(i)] = {
                "SS_delay"  : int(grows["SS_delay"].iloc[i]),
                "SS_amount" : float(grows["SS_amount"].iloc[i]),
                "LL_delay"  : int(grows["LL_delay"].iloc[i]),
                "LL_amount" : float(grows["LL_amount"].iloc[i]),
                "pair_id"   : str(grows["pair_id"].iloc[i]),
                "block_id"  : str(grows["block_id"].iloc[i]),
                "currency"  : str(grows["currency"].iloc[i]),
                }

    return(pair_dat)

class DiscountPage(Page):
    form_model   = "player"

    def get_form_fields(self):
        num_per_page = self.participant.vars["time_num_per_page"]
        form_fields =  ["choice_"    + str(i) for i in range(1, num_per_page + 1)]
        form_fields += ["timeStamps"]
        return form_fields

    def vars_for_template(self):
        rnum = self.round_number
        # Where is the session happening?
        locale = self.participant.vars["locale"]

        # Randomize the data if we're in the first round
        if rnum == 1 and "time_is_set" not in self.participant.vars:
            self.participant.vars["time_is_set"] = True
            # Record the choices for every round here
            self.participant.vars["time_choice"] = []
            # Record the block chosen and the pairs chosen
            self.participant.vars["time_blocks"] = []
            self.participant.vars["time_pairs"] = {}

        # Choose a block to use for this round without replacment
        blocks = self.participant.vars["time_blocks"]
        if len(blocks) == 0:
            block_to_use = random.choice(self.participant.vars["time_block_names"])
            blocks.append(block_to_use)
        elif len(blocks) < rnum:
            block_to_use = random.choice(self.participant.vars["time_block_names"])
            while block_to_use in blocks:
                block_to_use = random.choice(self.participant.vars["time_block_names"])
            blocks.append(block_to_use)
        else:
            block_to_use = blocks[rnum - 1]
        # Record the block ID
        setattr(self.player, "block_ID", block_to_use)

        time_pairs = self.participant.vars["time_pairs"]
        if len(time_pairs) < rnum:
            # The lottery data for this row
            pairdat = get_pairdat(self, block_to_use)
            time_pairs[block_to_use] = pairdat
        else:
            pairdat = time_pairs[block_to_use]

        # Record the pair IDs
        for i in range(1, self.participant.vars["time_num_per_page"] + 1):
            setattr(self.player, "pair_ID_"   + str(i), str(pairdat[str(i - 1)]["pair_id"]))

        # Make sure we don't reuse blocks across rounds
        self.participant.vars["time_blocks"] = blocks
        self.participant.vars["time_pairs"]  = time_pairs

        # Pass the start time to the Code
        stime = self.participant.vars["start_time"]
        if locale == "rsa":
            rsa_tz = tz.gettz("Africa/Johannesburg")
            stime = stime.astimezone(rsa_tz)
        elif locale == "usa":
            usa_tz = tz.gettz("America/New_York")
            stime = stime.astimezone(usa_tz)

        stime = [stime.strftime("%Y"),
                str(int(stime.strftime("%m")) - 1), # Javascript counts months from 0
                stime.strftime("%d"),
                stime.strftime("%H"),
                stime.strftime("%M"),]

        time_dat = {
                "round_number"    : rnum,
                "number_of_rounds": self.participant.vars["time_num_rounds"],
                "pairdat"         : pairdat,
                "hex_colors"      : self.participant.vars["time_hex_colors"],
                "task_number"     : 1,
                "num_per_page"    : self.participant.vars["time_num_per_page"],
                "start_time"      : stime,
               }

        return {
            "time_dat" : time_dat,
            "expiration_time": get_expiration_time(self),
            "video_url": get_video_url(self.participant.vars["locale"], Tasks.time),
        }

    def is_displayed(self):
        return self.round_number <= self.participant.vars["time_num_rounds"]

    def before_next_page(self):
        tchoice = [getattr(self.player, "choice_" + str(i)) for i in range(1, self.participant.vars["time_num_per_page"] + 1)]
        self.participant.vars["time_choice"] += [tchoice]

class Results(Page):
    def get_choice_for_payment(self):
        display_me = self.round_number == self.participant.vars["time_num_rounds"]

        if display_me and "time_pay_set" not in self.participant.vars:
            # Stuff we've been saving for each subject.
            blocks       = self.participant.vars["time_blocks"]
            time_pairs   = self.participant.vars["time_pairs"]
            time_choices = self.participant.vars["time_choice"]

            # Randomly select a block for payment
            pay_block_num = random.choice([i for i in range(0, len(blocks))])

            pay_block = blocks[pay_block_num]
            self.participant.vars["time_block_chosen"] = pay_block

            # Randomly select a pair from this block for payment
            pay_pair_num = random.choice(range(0, len(time_pairs[pay_block])))
            pay_pair = time_pairs[pay_block][str(pay_pair_num)]

            self.participant.vars["time_pair_chosen"] = pay_pair

            # Get the choices made by the subejcts to fill in the table
            self.participant.vars["time_pay_block"] = pay_block
            self.participant.vars["time_pay_block_num"] = pay_block_num
            self.participant.vars["time_pay_full_pairs"] = time_pairs[pay_block]
            self.participant.vars["time_pay_pair"] = pay_pair
            self.participant.vars["time_pay_pair_num"] = pay_pair_num
            self.participant.vars["time_pay_block_choices"] = time_choices[pay_block_num]
            # Don't select new payments on refresh
            self.participant.vars["time_pay_set"] = True

            setattr(self.player, "choice_for_payment", pay_pair["pair_id"])
            setattr(self.player, "block_for_payment",  pay_block)

        return(display_me)

    def vars_for_template(self):
        self.get_choice_for_payment()

        # Where are we?
        locale = self.participant.vars["locale"]

        pay_block_num = self.participant.vars["time_pay_block_num"]
        pairdat       = self.participant.vars["time_pay_full_pairs"]
        pay_pair      = self.participant.vars["time_pay_pair"]
        pay_pair_num  = self.participant.vars["time_pay_pair_num"]
        choices       = self.participant.vars["time_pay_block_choices"]

        pay_ss = "SS" if choices[pay_pair_num] == 0 else "LL"
        final_payment = {
                "currency": pay_pair["currency"],
                "amounts" : [pay_pair[pay_ss + "_amount"]],
                "when" : [pay_pair[pay_ss + "_delay"]],
                }
        self.participant.vars["time_final_payment"] = final_payment
        setattr(self.player, "final_payment", json.dumps(final_payment))

        # Pass the start time to the Code
        stime = self.participant.vars["start_time"]
        if locale == "rsa":
            rsa_tz = tz.gettz("Africa/Johannesburg")
            stime = stime.astimezone(rsa_tz)
        elif locale == "usa":
            usa_tz = tz.gettz("America/New_York")
            stime = stime.astimezone(usa_tz)

        stime = [stime.strftime("%Y"),
                str(int(stime.strftime("%m")) - 1), # Javascript counts months from 0
                stime.strftime("%d"),
                stime.strftime("%H"),
                stime.strftime("%M"),]

        time_dat = {
                "round_number"    : self.round_number,
                "number_of_rounds": self.participant.vars["time_num_rounds"],
                "hex_colors"      : self.participant.vars["time_hex_colors"],
                "pairdat"         : pairdat,
                "pay_block_num"   : pay_block_num,
                "pay_pair"        : pay_pair,
                "pay_pair_num"    : pay_pair_num,
                "choices"         : choices,
                "num_per_page"    : self.participant.vars["time_num_per_page"],
                "start_time"      : stime,
                "final_payment"   : final_payment,
               }

        # Save this data for use in the final results page
        self.participant.vars["time_results"] = time_dat

        return {
            "time_dat" : time_dat,
            "expiration_time": get_expiration_time(self),
        }

    def is_displayed(self):
        display_me = self.get_choice_for_payment()
        return display_me

class Intro(Page):
    def vars_for_template(self):
        table_details = task_sequence_table_info(self, Constants.app_name)
        return{
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
            "video_url": get_video_url(self.participant.vars['locale'], Tasks.time)
        }


page_sequence = [
    Intro,
    Instructions,
    DiscountPage,
    Results,
]
