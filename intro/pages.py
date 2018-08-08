from ._builtin import Page
from .models import Constants
from time import time
from common_helper_functions import task_sequence_table_info, format_datetime, get_expiration_time
from datetime import datetime
import re
from dateutil import tz


def type_reducer(val):
    try:
        return(int(val))
    except ValueError:
        try:
            return(float(val))
        except:
            return(str(val))

def set_participant_variables(page):
    plabel      = page.participant.label
    lookup_data = page.session.vars["lookup_data"]
    prow        = lookup_data.loc[lookup_data["participant_label"] == plabel]

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print("THIS MUST BE REMOVED FOR PRODUCTION!!!!!")
    # Need to get rid of the len(prow) check
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    if len(prow) > 0:
        for col in prow:
            # No need to keep track of these specific variables
            if col in ["ID", "participant_label", "link"]:
                continue
            elif col == "start_time" or col == "end_time":
                # Store the start time as a datetime variable
                time_val  = prow[col].iloc[0]
                dtime_val = datetime.strptime(time_val, "%Y-%m-%d %H:%M")
                # convert naive datetime to UTC
                dtime_val = dtime_val.replace(tzinfo=tz.UTC)
                page.participant.vars[col] = dtime_val
            else:
                # Everything else is put into the vars as their column names
                # Try and convert the value to either int or float, and failing that
                # make it a string
                val = type_reducer(prow[col].iloc[0])
                page.participant.vars[col] = val

    ###
    ### DEBUG ONLY! OVERWRITING START/STOP TIMES READ FROM FILE DURING DEBUGGING OF TIMER CODE CHANGES.
    ### PLACING HERE BECAUSE SET_DEFAULT_PVARS IS CALLED AT SESSION CREATION,
    ### AND WOULD BE OVERWRITTEN BY THE ABOVE CODE.
    ###

    print("**DEBUG** participant.vars.end_time from file: " + str(page.participant.vars["end_time"]))

    # debug_dt = datetime.strptime("2020-05-22 04:00", "%Y-%m-%d %H:%M")
    # debug_dt = debug_dt.replace(tzinfo=tz.UTC)
    page.participant.vars["start_time"] = datetime.strptime("2020-05-25 04:01", "%Y-%m-%d %H:%M").replace(tzinfo=tz.UTC)
    page.participant.vars["end_time"] = datetime.strptime("2020-05-26 03:59", "%Y-%m-%d %H:%M").replace(tzinfo=tz.UTC)
    print("**DEBUG** participant.vars.end_time overwrite: " + str(page.participant.vars["end_time"]))

    ###
    ###################################################################################################
    ###




class Setup(Page):
    # Using this function to setup some subject specific variables
    def is_displayed(self):
        set_participant_variables(self)
        return False

class Welcome(Page):
    def vars_for_template(self):
        # Set the locale on welcome
        self.player.locale = self.participant.vars["locale"]

        set_participant_variables(self)
        table_details = task_sequence_table_info(self, Constants.app_name)

        vars = {
            "formatted_end_time" : format_datetime(self),
            "app_sequence" : table_details['sequence'],
            "apps_completed" : table_details['num_tasks_completed'],
            "expiration_time" : get_expiration_time(self),
            }
        return vars


class GSUConsent(Page):
    form_model = 'player'
    form_fields = [
        'empty',
    ]

    def vars_for_template(self):
        set_participant_variables(self)

        return {}

    def is_displayed(self):
        return self.participant.vars["locale"] == "usa"


class UCTConsent(Page):
    form_model = 'player'
    form_fields = [
        'empty',
    ]

    def vars_for_template(self):
        return {}

    def is_displayed(self):
        return self.participant.vars["locale"] == "rsa"


class GSU_Overview(Page):
    form_model = 'player'
    form_fields = [
        'payment_primary',
        'payment_secondary',
        'payment_first_name',
        'payment_last_name',
        'payment_phone',
        'payment_phone_confirm',
        'payment_email',
        'payment_email_confirm',
        'payment_address_1',
        'payment_address_2',
        'payment_city',
        'payment_state',
        'payment_zip',
    ]

    def error_message(self, values):
        phone_number = re.compile("^[0-9]{10}$")
        if values['payment_primary'] == 'venmo' or values['payment_secondary'] == 'venmo':
            if values['payment_phone'] is None or values['payment_phone_confirm'] is None:
                return 'Phone number must not be blank'
            if phone_number.match(values['payment_phone']) is None:
                return "Phone numbers must be 10 digits"
            if values['payment_phone'] != values['payment_phone_confirm']:
                return 'Phone numbers must match'
        if values['payment_primary'] == 'paypal' or values['payment_secondary'] == 'paypal':
            if values['payment_email'] is None or values['payment_email_confirm'] is None:
                return 'Email must not be blank'
            if values['payment_email'] != values['payment_email_confirm']:
                return 'Emails must match'
        if values['payment_primary'] == 'check' or values['payment_secondary'] == 'check':
            if values['payment_address_1'] is None:
                return 'Address line 1 must not be blank'
            if values['payment_city'] is None:
                return 'City must not be blank'
            if values['payment_state'] is None:
                return 'State must not be blank'
            if values['payment_zip'] is None:
                return 'Zip code must not be blank'

    def vars_for_template(self):
        return {"expiration_time" : get_expiration_time(self) }

    def is_displayed(self):
        return self.participant.vars["locale"] == "usa"

    def before_next_page(self):
        # user must complete tasks within a certain amount of time
        payment_method = {
                'payment_secondary'  : self.player.payment_secondary,
                'payment_primary'    : self.player.payment_primary,
                'payment_first_name' : self.player.payment_first_name,
                'payment_last_name'  : self.player.payment_last_name,
                'payment_phone'      : self.player.payment_phone,
                'payment_email'      : self.player.payment_email,
                'payment_address_1'  : self.player.payment_address_1,
                'payment_address_2'  : self.player.payment_address_2,
                'payment_city'       : self.player.payment_city,
                'payment_state'      : self.player.payment_state,
                'payment_zip'        : self.player.payment_zip,
        }
        self.participant.vars['payment_method'] = payment_method


class UCT_Overview(Page):
    form_model = 'player'
    form_fields = [
        'payment_phone',
        'payment_phone_confirm',
    ]

    def error_message(self, values):
        phone_number = re.compile("^[0-9]{10}$")

        if values['payment_phone'] is None or values['payment_phone_confirm'] is None:
            return 'Phone number must not be blank'
        if phone_number.match(values['payment_phone']) is None:
            return "Phone numbers must be 10 digits"
        if values['payment_phone'] != values['payment_phone_confirm']:
            return 'Phone numbers must match'

    def before_next_page(self):
        # user must complete tasks within a certain amount of time
        payment_method = {
                'payment_secondary'  : self.player.payment_secondary,
                'payment_primary'    : self.player.payment_primary,
                'payment_first_name' : self.player.payment_first_name,
                'payment_last_name'  : self.player.payment_last_name,
                'payment_phone'      : self.player.payment_phone,
                'payment_email'      : self.player.payment_email,
                'payment_address_1'  : self.player.payment_address_1,
                'payment_address_2'  : self.player.payment_address_2,
                'payment_city'       : self.player.payment_city,
                'payment_state'      : self.player.payment_state,
                'payment_zip'        : self.player.payment_zip,
        }
        self.participant.vars['payment_method'] = payment_method

    def vars_for_template(self):
        return {"expiration_time" : get_expiration_time(self) }

    def is_displayed(self):
        return self.participant.vars["locale"] == "rsa"

page_sequence = [
        Setup,
        GSUConsent,
        UCTConsent,
        GSU_Overview,
        UCT_Overview,
        Welcome,
        ]
