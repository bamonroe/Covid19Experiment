from ._builtin import Page, WaitPage
from .models import Constants, get_pvar
import pandas as pd
import random
from common_helper_functions import task_sequence_table_info, get_expiration_time, get_video_url, Tasks

import json

def randomize_dat(dat):
    # Group each question by the group ID
    groups = {gid : rows for gid, rows in dat.groupby('lgid', sort=False)}
    # Randomize the rows in the groups if thir lgid is positive
    # This allows some groups to have non-random lottery orders
    out_groups = {}
    for i in groups:
        g = groups[i]
        rows = [i for i in range(0, len(g))]
        if i >= 0:
            random.shuffle(rows)
        out_groups[i] = dat.iloc[rows]

    # Sort the groups by absolute value of the lgid
    gkeys = {abs(k) : k for k in groups}

    fkeys = [i for i in gkeys.keys()]
    fkeys.sort()

    # Make the groups ordered by the abs of lgid
    out_list = [out_groups[gkeys[i]] for i in fkeys]

    # Concatenate the groups back into one dataset
    out_dat = pd.concat(out_list)
    return out_dat

# This function changes a number from a float to int if possible
def collapse_numeric(x):
    y = float(x)
    if y % 1 == 0:
        out = int(y)
    else:
        out = y
    return out

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

def don_convert(don, num_ops):
    don = don if don != "nan" else -1
    don = float(don)
    if don == 0.5:
        don = [i for i in range(0, num_ops + 1)]
    elif don < 0:
        don = []
    else:
        don = [int(don)]
    return don

def get_lotdat(page_obj, rnum):
    num_ops = page_obj.participant.vars["risk_num_ops"]
    nrange = [str(x) for x in range(0, num_ops + 1)]

    # First get the column names of the input data
    aprob   = ["pA" + x for x in nrange]
    bprob   = ["pB" + x for x in nrange]
    aevents = ["pA" + x + "_events" for x in nrange]
    bevents = ["pB" + x + "_events" for x in nrange]
    aout    = ["A"  + x for x in nrange]
    bout    = ["B"  + x for x in nrange]
    alab    = ["label_A" + x for x in nrange]
    blab    = ["label_B" + x for x in nrange]
    acap    = ["caption_A" + x for x in nrange]
    bcap    = ["caption_B" + x for x in nrange]
    atop    = ["A_top"]
    btop    = ["B_top"]
    adon    = ["A_don"]
    bdon    = ["B_don"]

    # Get the particular row from the input data associated with this locale
    risk_dat = page_obj.participant.vars["risk_dat"]

    row = risk_dat.iloc[rnum - 1, :]

    # Turn the names into the values
    aprob = row[aprob].tolist()
    bprob = row[bprob].tolist()

    aevents = row[aevents].tolist()
    bevents = row[bevents].tolist()

    aevents = events_to_range(aevents)
    bevents = events_to_range(bevents)

    aout  = row[aout].tolist()
    bout  = row[bout].tolist()

    alab  = row[alab].tolist()
    blab  = row[blab].tolist()

    acap  = row[acap].tolist()
    bcap  = row[bcap].tolist()

    atop  = str(row[atop][0])
    btop  = str(row[btop][0])

    atop = atop if atop != "nan" else "&nbsp;"
    btop = btop if btop != "nan" else "&nbsp;"

    adon = don_convert(str(row[adon][0]), num_ops)
    bdon = don_convert(str(row[bdon][0]), num_ops)

    currency_symbol = row["currency_symbol"]

    # Make sure everything is in data types is understood by json
    aout = [str(collapse_numeric(out)) for out in aout]
    bout = [str(collapse_numeric(out)) for out in bout]

    aprob = [str(prob) for prob in aprob]
    bprob = [str(prob) for prob in bprob]

    acap = [str(out) for out in acap]
    bcap = [str(out) for out in bcap]

    acap = [str(out) for out in acap]
    bcap = [str(out) for out in bcap]

    lotdat = { "lotA": { "probabilities"     : aprob,
                         "prob_labels"       : alab,
                         "caption"           : acap,
                         "outcomes"          : aout,
                         "top_header"        : atop,
                         "double_or_nothing" : adon,
                         "events"            : aevents,
                       },
               "lotB": { "probabilities"     : bprob,
                         "prob_labels"       : blab,
                         "caption"           : bcap,
                         "outcomes"          : bout,
                         "top_header"        : btop,
                         "double_or_nothing" : bdon,
                         "events"            : bevents,
                       },
               "currency":   str(currency_symbol),
               "num_events": int(row["num_events"]),
               "lotid":      str(row["luid"]),
             }
    return lotdat

class LotteryPage(Page):
    form_model  = "player"
    form_fields = ["choice", "timeStamps"]
    def vars_for_template(self):
        rnum = self.round_number
        # Initialize some things in the first round
        if rnum == 1 and "risk_is_set" not in self.participant.vars:
            self.participant.vars["risk_is_set"] = True
            # Record the choices for every round here
            self.participant.vars["risk_choice"] = []
            # Randomize the data if we're in the first round
            locale = self.participant.vars["locale"]
            dat    = self.session.vars[locale + "_risk_dat"]
            self.participant.vars["risk_dat"] = randomize_dat(dat)

        # The lottery data for this row
        lotdat = get_lotdat(self, rnum)

        # Save the lottery ID
        setattr(self.player, "lot_id", lotdat["lotid"])

        risk_dat = {
                "round_number" : rnum,
                 "number_of_rounds": self.participant.vars["risk_num_rounds"],
                 "hex_colors": self.participant.vars["risk_hex_colors"],
                 "num_ops": self.participant.vars["risk_num_ops"],
                 "options" : ["A", "B"],
                 "lotdat": lotdat,
                }

        retd = {
            "risk_dat"        : risk_dat,
            "expiration_time" : get_expiration_time(self),
            "video_url"       : get_video_url(self.participant.vars["locale"], Tasks.risk),
        }
        return retd

    def before_next_page(self):
        self.participant.vars["risk_choice"].append(self.player.choice)

    def is_displayed(self):
        val = self.round_number <= self.participant.vars["risk_num_rounds"]
        return val

class Results(Page):
    form_model  = "player"
    form_fields = []

    def get_choice_for_payment(self):
        display_me = self.round_number == self.participant.vars["risk_num_rounds"]
        if display_me and "risk_pay_id" not in self.participant.vars:

            choice_num = random.choice(range(1, len(self.participant.vars["risk_choice"]) + 1))
            self.participant.vars["risk_pay_id"] = choice_num

            # Number of possible outcomes
            num_ops = self.participant.vars["risk_num_ops"]
            # The lottery dat for the randomly chosen lottery
            lotdat = get_lotdat(self, choice_num)
            # The number of events that will determine the outcome
            num_events = lotdat["num_events"]
            # Choose a number at random from the num_events
            random_number_for_payment = [i for i in range(1, num_events + 1)]
            random_number_for_payment = random.choice(random_number_for_payment)
            # Get the pair chosen for payment
            pair_for_payment = self.participant.vars["risk_choice"][choice_num - 1]
            # Which lottery did the subject choose
            lot_chosen = "lotA" if pair_for_payment == 0  else "lotB"
            # Get the lotdat for the chosen lottery
            chosen_lotdat = lotdat[lot_chosen]
            # Get the events from this lottery
            events = chosen_lotdat["events"]
            # Using the random_number_for_payment, which outcome has been chosen
            pay_outcome_num = [i for i in range(0, num_ops + 1) if random_number_for_payment in events[i]][0]
            # Get the outcome for payment
            pay_outcome = chosen_lotdat["outcomes"][pay_outcome_num]
            # Check for double_or_nothing
            don_outcomes = chosen_lotdat["double_or_nothing"]
            is_don = pay_outcome_num in don_outcomes
            # Choose a number at random from the num_events
            random_number_for_don = random.choice([0, 1])
            pay_double = random_number_for_don == 1

            if is_don:
                if pay_double:
                    final_payment = float(pay_outcome) * 2
                else:
                    final_payment = 0
            else:
                final_payment = pay_outcome

            final_payment = {
                    "currency": lotdat["currency"],
                    "amounts" : [final_payment],
                    "when"    : [0],
                    }

            # Save all this in participant vars
            self.participant.vars["risk_pay_random_number"] = random_number_for_payment
            self.participant.vars["risk_pay_outcome_num"] = pay_outcome_num
            self.participant.vars["risk_pay_outcome"]     = pay_outcome
            self.participant.vars["risk_don_outcomes"]    = don_outcomes
            self.participant.vars["risk_is_don"]          = is_don
            self.participant.vars["risk_don_number"]      = random_number_for_don
            self.participant.vars["risk_final_payment"]   = final_payment

        return(display_me)

    def vars_for_template(self):
        self.get_choice_for_payment()

        pair_for_payment   = self.participant.vars["risk_pay_id"]
        choice_for_payment = self.participant.vars["risk_choice"][pair_for_payment - 1]
        lotdat             = get_lotdat(self, pair_for_payment)

        random_number_for_payment = self.participant.vars["risk_pay_random_number"]
        pay_outcome_num       = self.participant.vars["risk_pay_outcome_num"]
        pay_outcome           = self.participant.vars["risk_pay_outcome"]
        is_don                = self.participant.vars["risk_is_don"]
        random_number_for_don = self.participant.vars["risk_don_number"]
        final_payment         = self.participant.vars["risk_final_payment"]

        # Save the data needed
        setattr(self.player, "pair_for_payment",   pair_for_payment)
        setattr(self.player, "choice_for_payment", choice_for_payment)
        setattr(self.player, "roll_for_payment",   random_number_for_payment)
        setattr(self.player, "final_payment",     json.dumps(final_payment))

        risk_dat = {
                "num_ops"     : self.participant.vars["risk_num_ops"],
                "hex_colors"  : self.participant.vars["risk_hex_colors"],
                "options"     : ["A", "B"],
                "lotdat"      : lotdat,
                "pair_for_payment"     : pair_for_payment,
                "choice_for_payment"   : choice_for_payment,
                "pay_outcome_num"      : pay_outcome_num,
                "pay_outcome"          : pay_outcome,
                "is_don"               : is_don,
                "random_number_for_pay": random_number_for_payment,
                "random_number_for_don": random_number_for_don,
                "final_payment"        : final_payment,
                }

        # Save this data for use with the final results page
        self.participant.vars["risk_results"] = risk_dat

        return {
            "risk_dat" : risk_dat,
            "expiration_time": get_expiration_time(self),
        }

    def is_displayed(self):
        return self.get_choice_for_payment()

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
            "video_url"            : get_video_url(self.participant.vars['locale'], Tasks.risk)
        }

page_sequence = [
    Intro,
    Instructions,
    LotteryPage,
    Results,
]
