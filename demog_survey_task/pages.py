from . import models

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otreeutils.surveys import SurveyPage, setup_survey_pages
from otreeutils.pages import ExtendedPage
from common_helper_functions import task_sequence_table_info, get_expiration_time

# to enable random responses for testing:
# 1. in settings.py add this line: APPS_DEBUG = True
# 2. in each page class below add this line: debug_fill_forms_randomly = True




class Intro(Page):
    def vars_for_template(self):
        table_details = task_sequence_table_info(self, Constants.app_name)
        return {
            "app_sequence": table_details['sequence'],
            "apps_completed": table_details['num_tasks_completed'],
            "expiration_time": get_expiration_time(self),
        }


class SurveyPage_General_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


class SurveyPage_USA_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return  self.participant.vars["locale"] == "usa"


class SurveyPage_RSA_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return self.participant.vars["locale"] == "rsa"


class SurveyPage_USA_2(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return self.participant.vars["locale"] == "usa"


class SurveyPage_General_2(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


class SurveyPage_General_3(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


survey_pages = [
    SurveyPage_General_1,
    SurveyPage_USA_1,
    SurveyPage_RSA_1,
    SurveyPage_USA_2,
    SurveyPage_General_2,
    SurveyPage_General_3,
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    Intro,  # define some pages that come before the survey
    # ...
]

# add the survey pages to the page sequence list
page_sequence.extend(survey_pages)

# add more pages that come after the survey:
# page_sequence.extend([AnotherPage, ...])
