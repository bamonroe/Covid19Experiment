from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd
import pathlib
from datetime import datetime, timedelta, timezone
from dateutil import tz
from common_helper_functions import set_default_pvars
from dateutil import tz

import json

def final_pay_to_csv(pay):

    payfile = pathlib.Path("payfiles/" + pay["plabel"] + "_payinfo.csv")
    if payfile.exists():
        return

    # Add basic stuff
    dat = [
           pay["plabel"],     pay["locale"],   pay["wave"],        pay["endowment"],
           pay["start_time"], pay["end_time"], pay["finish_time"], pay["finish_on_time"],
           pay["payment_method"]["payment_primary"],
           pay["payment_method"]["payment_secondary"],
           pay["payment_method"]["payment_first_name"],
           pay["payment_method"]["payment_last_name"],
           pay["payment_method"]["payment_phone"],
           pay["payment_method"]["payment_email"],
           pay["payment_method"]["payment_address_1"],
           pay["payment_method"]["payment_address_2"],
           pay["payment_method"]["payment_city"],
           pay["payment_method"]["payment_state"],
           pay["payment_method"]["payment_zip"]
          ]

    # Add beliefs
    bel_labs =  ["amounts", "when", "qid", "gid", "choices"]
    bel_vals =  [pay["beliefs"][k] for k in bel_labs if k is not "choices"]
    bel_vals =  [b[0] if len(b) > 0 else 0 for b in bel_vals]
    bel_vals += [";".join([str(c) for c in pay["beliefs"]["choices"]])]
    bel_labs =  ["beliefs_" + b for b in bel_labs]
    dat += bel_vals

    # Add risk
    risk_labs = ["amounts", "when"]
    risk_vals = [pay["risk"][k] for k in risk_labs]
    risk_vals = [b[0] if len(b) > 0 else 0 for b in risk_vals]
    risk_labs = ["risk_" + r for r in risk_labs]
    dat += risk_vals

    # Add time
    time_labs = ["amounts", "when"]
    time_vals = [pay["time"][k] for k in time_labs]
    time_vals = [b[0] if len(b) > 0 else 0 for b in time_vals]
    time_labs = ["time_" + r for r in time_labs]
    dat += time_vals

    # Add CA
    ca_labs = ["amounts", "when"]
    ca_vals0 = [pay["ca"][k][0] for k in ca_labs]
    ca_labs0 = ["ca_" + r + "0"   for r in ca_labs]
    ca_vals1 = [pay["ca"][k][1] for k in ca_labs]
    ca_labs1 = ["ca_" + r + "1"   for r in ca_labs]
    dat += ca_vals0
    dat += ca_vals1

    full_labs  = ["plabel", "locale", "wave", "endowment"]
    full_labs += ["start_time", "end_time", "finish_time","finish_on_time"]
    full_labs += [
            "payment_primary", "payment_secondary", "payment_first_name", "payment_last_name",
            "payment_phone", "payment_email", "payment_address_1",
            "payment_address_2", "payment_city", "payment_state",
            "payment_zip"]

    full_labs += bel_labs
    full_labs += risk_labs
    full_labs += time_labs
    full_labs += ca_labs0
    full_labs += ca_labs1

    df = pd.DataFrame([dat], columns = full_labs)

    for w in ["risk_when", "time_when", "ca_when0", "ca_when1"]:
        # add_days = timedelta(days = int(df[w].iloc[0]))
        # pay_day  = start_time + add_days
        # df[w].iloc[0] = pay_day.strftime("%Y-%m-%d %H:%M")
        dt = datetime.strptime(df[w].iloc[0], '%d %B %Y')
        dt = dt.replace(tzinfo=tz.UTC)
        df[w].iloc[0] = dt

    print(df)

    df.to_csv(payfile, index = False, index_label = False)

class FinalPage(Page):
    form_model  = "player"
    def vars_for_template(self):

        # Where are we
        locale = self.participant.vars["locale"]

        start_time = self.participant.vars["start_time"]
        if locale == "rsa":
            rsa_tz = tz.gettz("Africa/Johannesburg")
            start_time = start_time.astimezone(rsa_tz)
        elif locale == "usa":
            usa_tz = tz.gettz("America/New_York")
            start_time = start_time.astimezone(usa_tz)

        ## DEBUG
        set_default_pvars(self)
        if self.participant.label == None:
            self.participant.label = "test_subject"

        if "utc_finish_time" not in self.participant.vars:
            # What time is it right now in utc
            self.participant.vars["utc_finish_time"] = datetime.now(tz=timezone.utc)

            risk_results    = self.participant.vars["risk_results"]
            time_results    = self.participant.vars["time_results"]
            ca_results      = self.participant.vars["ca_results"]
            beliefs_results = self.participant.vars["beliefs_results"]


            risk_when = risk_results["final_payment"]["when"][0]
            time_when = time_results["final_payment"]["when"][0]
            ca0_when  = ca_results["final_payment"]["when"][0]
            ca1_when  = ca_results["final_payment"]["when"][1]

            risk_when = start_time + timedelta(days = risk_when)
            time_when = start_time + timedelta(days = time_when)
            ca0_when  = start_time + timedelta(days = ca0_when)
            ca1_when  = start_time + timedelta(days = ca1_when)

            risk_when = risk_when.strftime("%d %B %Y")
            time_when = time_when.strftime("%d %B %Y")
            ca0_when  = ca0_when.strftime("%d %B %Y")
            ca1_when  = ca1_when.strftime("%d %B %Y")

            risk_results["final_payment"]["when"][0] = risk_when
            time_results["final_payment"]["when"][0] = time_when
            ca_results["final_payment"]["when"][0]   = ca0_when
            ca_results["final_payment"]["when"][1]   = ca1_when
            ca_results["final_payment"]["is_date"]   = True

            self.participant.vars["risk_results"]    = risk_results
            self.participant.vars["time_results"]    = time_results
            self.participant.vars["ca_results"]      = ca_results
            self.participant.vars["beliefs_results"] = beliefs_results

        risk_results    = self.participant.vars["risk_results"]
        time_results    = self.participant.vars["time_results"]
        ca_results      = self.participant.vars["ca_results"]
        beliefs_results = self.participant.vars["beliefs_results"]

        beliefs_final_payment = self.participant.vars["beliefs_final_payment"]
        risk_final_payment    = self.participant.vars["risk_final_payment"]
        time_final_payment    = self.participant.vars["time_final_payment"]
        ca_final_payment      = self.participant.vars["ca_final_payment"]
        endowment             = self.participant.vars["endowment"]

        # Subjects have finished on time if their finish_time precedes the end time
        end_time       = self.participant.vars["end_time"]
        finish_time    = self.participant.vars["utc_finish_time"]
        print("subject finish time: " + str(finish_time))
        print("session end time: " + str(end_time))
        finish_on_time = finish_time < end_time
        setattr(self.player, "finish_time", str(finish_time))

        # Start time just to find

        full_final_pay = {
                "plabel"         : self.participant.label,
                "locale"         : locale,
                "wave"           : self.participant.vars["wave"],
                "start_time"     : start_time.strftime("%Y-%m-%d %H:%M"),
                "end_time"       : self.participant.vars["end_time"].strftime("%Y-%m-%d %H:%M"),
                "finish_time"    : self.participant.vars["utc_finish_time"].strftime("%Y-%m-%d %H:%M"),
                "finish_on_time" : finish_on_time,
                "endowment"      : endowment,
                "beliefs"        : beliefs_final_payment,
                "risk"           : risk_final_payment,
                "time"           : time_final_payment,
                "ca"             : ca_final_payment,
                "payment_method" : self.participant.vars["payment_method"],
                }

        self.player.final_pay = json.dumps(full_final_pay)
        # Save the final_pay for the subject to a CSV
        final_pay_to_csv(full_final_pay)

        final_dat = {
            "session_date"     : start_time.strftime("%d %B %Y"),
            "endowment" : endowment,
            "risk_dat": risk_results,
            "time_dat": time_results,
            "ca_dat": ca_results,
            "beliefs_dat": beliefs_results,
            "finish_on_time": finish_on_time
            }
        return final_dat

    def is_displayed(self):
        return True

page_sequence = [
    FinalPage,
]
