from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import pandas as pd
from common_helper_functions import set_default_pvars, format_datetime

author = 'Your name here'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'intro'
    players_per_group = None
    num_rounds = 1
    app_name = 'intro'

class Subsession(BaseSubsession):
    def creating_session(self):
        treatment = self.session.config["treatment"]
        wave = self.session.config["wave"]
        lookup_data = pd.read_csv("configs/w" + str(wave) + "t" + str(treatment) + "_lookup.csv")
        self.session.vars["lookup_data"] = lookup_data
        for p in self.get_players():
            set_default_pvars(p)

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    empty = models.StringField(blank=True)

    def empty_error_message(self, value):
        from datetime import datetime, timezone

        if datetime.now(tz=timezone.utc) < self.participant.vars['start_time']:
            # Then session has not started yet
            from dateutil import tz
            locale = self.participant.vars["locale"]

            rsa_time_format = "%H:%M "
            usa_time_format = "%I:%M %p "

            if locale == "rsa":
                date_display_format = "in South Africa on %A, %B %d, %Y"
            elif locale == 'usa':
                date_display_format = "in Atlanta, Georgia on %A, %B %d, %Y"

            if locale == "rsa":
                datetime_display_format = rsa_time_format + date_display_format
                rsa_tz = tz.gettz("Africa/Johannesburg")
                start_time_for_display = self.participant.vars["start_time"].astimezone(rsa_tz).strftime(datetime_display_format)
            elif locale == "usa":
                datetime_display_format = usa_time_format + date_display_format
                usa_tz = tz.gettz("America/New_York")
                start_time_for_display = self.participant.vars["start_time"].astimezone(usa_tz).strftime(
                    datetime_display_format)
            else:
                start_time_for_display = self.participant.vars["start_time"]

            return 'You may not begin the study until ' + start_time_for_display + '.'

    payment_first_name=models.StringField(label="First name:")
    payment_last_name=models.StringField(label="Last name:")

    payment_primary=models.StringField(
        label="Primary payment method:",
        choices=(
            ('venmo',  'Venmo'),
            ('paypal', 'Paypal'),
        )
    )

    payment_secondary=models.StringField(
        label="Secondary payment method (optional):",
        choices=(
            ('venmo',  'Venmo'),
            ('paypal', 'Paypal'),
        ),
        blank=True,
    )

    # Venmo fields
    payment_phone = models.StringField(label="Phone number (please enter your number in this format 0821234567):",
                                       blank=True)
    payment_phone_confirm = models.StringField(label="Confirm phone number:", blank=True)

    # Paypal fields
    payment_email = models.StringField(label="Email:", blank=True)
    payment_email_confirm = models.StringField(label="Confirm email:", blank=True)

    # Check fields
    payment_address_1 = models.StringField(label="Address line 1:", blank=True)
    payment_address_2 = models.StringField(label="Address line 2 (optional):", blank=True)
    payment_city = models.StringField(label="City:", blank=True)
    payment_state = models.StringField(label="State:", blank=True)
    payment_zip = models.StringField(label="Zip code:", blank=True)

    # Some basic data
    locale = models.StringField(default = "")
