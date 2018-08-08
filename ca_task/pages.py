from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd
import random
import json
from .models import Constants
from common_helper_functions import task_sequence_table_info, get_expiration_time, get_video_url, Tasks
from dateutil import tz

def get_opt_chosen(choice, top_opt):
    # Top and bottom are randomized
    choice = str(choice)
    if choice == "0" and top_opt == "A":
        opt_chosen = "A"
    elif choice == "0" and top_opt == "B":
        opt_chosen = "B"
    elif choice == "1" and top_opt == "A":
        opt_chosen = "B"
    elif choice == "1" and top_opt == "B":
        opt_chosen = "A"
    return opt_chosen

def events_to_range(events):
    out = []
    max_val = 0
    for e in events:
        if e == 0:
            out.append([])
            continue
        i = max_val + 1
        k = [j for j in range(i, max_val + e + 1)]
        out.append(k)
        max_val = max(k)
    return out

def get_pairdat(page_obj, pairs):
    # Get the data from the constants model
    locale = page_obj.participant.vars["locale"]
    dat    = page_obj.session.vars[locale + "_ca_dat"]

    # Get a random row that hasn't been used
    used_ids = [d["pair_id"] for d in pairs]
    full_ids = dat["pair_id"].unique()

    rows = [i for i in full_ids if str(i) not in used_ids]
    row  = random.choice(rows)
    # Get these actual row
    grows = dat.loc[dat["pair_id"] == row]

    num_events = int(grows["num_events"].iloc[0])

    p0_events = int(grows["p0_events"].iloc[0])
    p1_events = int(grows["p1_events"].iloc[0])

    p0 = p0_events / num_events
    p1 = p1_events / num_events

    p0_label = str(grows["p0_label"].iloc[0])
    p1_label = str(grows["p1_label"].iloc[0])

    p0_caption = str(grows["p0_caption"].iloc[0])
    p1_caption = str(grows["p1_caption"].iloc[0])

    SS_delay = int(grows["SS"].iloc[0])
    LL_delay = int(grows["LL"].iloc[0])

    option_A = {
            "S0" : float(grows["SA0"].iloc[0]),
            "S1" : float(grows["SA1"].iloc[0]),
            "L0" : float(grows["LA0"].iloc[0]),
            "L1" : float(grows["LA1"].iloc[0]),
            }

    option_B = {
            "S0" : float(grows["SB0"].iloc[0]),
            "S1" : float(grows["SB1"].iloc[0]),
            "L0" : float(grows["LB0"].iloc[0]),
            "L1" : float(grows["LB1"].iloc[0]),
            }

    pair_dat = {
            "option_A" : option_A,
            "option_B" : option_B,
            "SS_delay" : SS_delay,
            "LL_delay" : LL_delay,
            "top_opt" : random.choice(["A", "B"]),
            "p0"  : p0,
            "p1"  : p1,
            "p0_events"   : p0_events,
            "p1_events"   : p1_events,
            "p0_label"   : p0_label,
            "p1_label"   : p1_label,
            "p0_caption" : p0_caption,
            "p1_caption" : p1_caption,
            "num_events" : num_events,
            "pair_id"  : str(grows["pair_id"].iloc[0]),
            "currency"  : str(grows["currency"].iloc[0]),
                }

    return(pair_dat)

class Intro(Page):
    def vars_for_template(self):
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
            "video_url"      : get_video_url(self.participant.vars["locale"], Tasks.ca)
        }

class TaskPage(Page):
    form_model  = "player"
    form_fields = ["choice", "timeStamps"]

    def vars_for_template(self):
        rnum = self.round_number
        # Where is the session happening?
        locale = self.participant.vars["locale"]
        # Randomize the data if we're in the first round
        if rnum == 1 and "ca_is_set" not in self.participant.vars:
            self.participant.vars["ca_is_set"] = True
            # Record the choices for every round here
            self.participant.vars["ca_choice"] = []
            # Record the pairs used
            self.participant.vars["ca_pairs"] = []

        # Choose a pair for this round without replacment
        pairs = self.participant.vars["ca_pairs"]

        if len(pairs) < rnum:
            # The lottery data for this row
            pairdat = get_pairdat(self, pairs)
            pairs.append(pairdat)
        else:
            pairdat = pairs[rnum - 1]

        # Save the pair ID chosen
        setattr(self.player, "pair_ID", str(pairdat["pair_id"]))
        # Top and bottom are randomized
        setattr(self.player, "top_option", pairdat["top_opt"])

        # Make sure we don't reuse blocks across rounds
        self.participant.vars["ca_pairs"] = pairs

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

        ca_dat = {
                "round_number"    : rnum,
                "number_of_rounds": self.participant.vars["ca_num_rounds"],
                "pairdat"         : pairdat,
                "hex_colors"      : self.participant.vars["ca_hex_colors"],
                "task_number"     : 5,
                "top_bot"         : ["t", "b"],
                "start_time"      : stime,
               }

        return {
            "ca_dat" : ca_dat,
            "expiration_time": get_expiration_time(self),
            "video_url": get_video_url(self.participant.vars["locale"], Tasks.ca),
        }

    def is_displayed(self):
        return self.round_number <= self.participant.vars["ca_num_rounds"]

    def before_next_page(self):
        choice  = getattr(self.player, "choice")
        top_opt = getattr(self.player, "top_option")

        # Top and bottom are randomized
        opt_chosen = get_opt_chosen(choice, top_opt)

        setattr(self.player, "choice", opt_chosen)
        self.participant.vars["ca_choice"].append(choice)

class Results(Page):
    form_model  = "player"

    def get_payment(self):
        if "ca_pay_is_set" not in self.participant.vars:
            self.participant.vars["ca_pay_is_set"] = True
            # Choose a pair for this round without replacment
            pairs    = self.participant.vars["ca_pairs"]
            pay_pair_num = random.choice([i for i in range(0, len(pairs))])

            # Both pairs have the same percentages for outcomes, so select an outcome
            pairs  = self.participant.vars["ca_pairs"]
            pay_pair = pairs[pay_pair_num]

            p0_events = pay_pair["p0_events"]
            p1_events = pay_pair["p1_events"]
            num_events = pay_pair["num_events"]
            events = events_to_range([p0_events, p1_events])
            rand_num_for_payment = random.choice([i for i in range(1, num_events + 1)])

            rand_outcome = [i for i in [0, 1] if rand_num_for_payment in events[i]][0]

            self.participant.vars["ca_pair_num"] = pay_pair_num
            self.participant.vars["ca_rand_outcome"] = rand_outcome
            self.participant.vars["ca_rand_num_for_payment"] = rand_num_for_payment

    def vars_for_template(self):
        # Set the outcomes for payment
        self.get_payment()
        # The round number
        rnum = self.round_number
        # Where are we?
        locale = self.participant.vars["locale"]

        # Make sure we don't reuse blocks across rounds
        pairs    = self.participant.vars["ca_pairs"]
        pay_pair_num = self.participant.vars["ca_pair_num"]
        pair_for_payment = pairs[pay_pair_num]

        choices = self.participant.vars["ca_choice"]
        choice_for_pay = choices[pay_pair_num]

        rand_num_for_payment = self.participant.vars["ca_rand_num_for_payment"]
        outcome_for_payment = self.participant.vars["ca_rand_outcome"]

        # Top and bottom are randomized
        top_opt = pair_for_payment["top_opt"]

        opt_chosen = get_opt_chosen(choice_for_pay, top_opt)

        outcome_set_for_payment = "option_" + opt_chosen
        outcome_set_for_payment = pair_for_payment[outcome_set_for_payment]

        SS_payment = outcome_set_for_payment["S"+ str(outcome_for_payment)]
        LL_payment = outcome_set_for_payment["L"+ str(outcome_for_payment)]

        final_payment = {
                "currency": pair_for_payment["currency"],
                "amounts": [SS_payment, LL_payment],
                "when": [pair_for_payment["SS_delay"], pair_for_payment["LL_delay"]],
                "is_date": False,
                }
        self.participant.vars["ca_final_payment"] = final_payment

        # Save the payment info and the choice for payment to the dataset
        setattr(self.player, "final_payment", json.dumps(final_payment))
        setattr(self.player, "choice_for_payment", pay_pair_num)

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


        ca_dat = {
                "round_number"    : rnum,
                "number_of_rounds": self.participant.vars["ca_num_rounds"],
                "hex_colors"      : self.participant.vars["ca_hex_colors"],
                "pairdat"         : pair_for_payment,
                "pair_for_pay"    : pay_pair_num,
                "choice_for_pay"  : choice_for_pay,
                "rand_num_for_payment" : rand_num_for_payment,
                "task_number"     : 5,
                "top_bot"         : ["t", "b"],
                "final_payment"   : final_payment,
                "start_time"      : stime,
               }

        # Save this data for use with the final results page
        self.participant.vars["ca_results"] = ca_dat

        return {
            "ca_dat": ca_dat,
            "expiration_time": get_expiration_time(self),
        }

    def is_displayed(self):
        return self.round_number == self.participant.vars["ca_num_rounds"]

page_sequence = [
    Intro,
    Instructions,
    TaskPage,
    Results,
]
