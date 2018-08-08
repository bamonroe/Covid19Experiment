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


class SurveyPage_HSRC_General_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


class SurveyPage_HSRC_USA_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return self.participant.vars["locale"] == "usa"


class SurveyPage_HSRC_RSA_1(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return self.participant.vars["locale"] == "rsa"


class SurveyPage_HSRC_General_2(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


class SurveyPage_HSRC_General_3(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


# The following page displays only if at least one problem was indicated on the prior page.
class SurveyPage_HSRC_General_3b(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return (self.player.anxiety_nervous is not None and self.player.anxiety_nervous != 1) or \
               (self.player.anxiety_worry_uncontrolled is not None and self.player.anxiety_worry_uncontrolled != 1) or \
               (self.player.anxiety_worry_multiple is not None and self.player.anxiety_worry_multiple != 1) or \
               (self.player.anxiety_relax is not None and self.player.anxiety_relax != 1) or \
               (self.player.anxiety_restless is not None and self.player.anxiety_restless != 1) or \
               (self.player.anxiety_irritable is not None and self.player.anxiety_irritable != 1) or \
               (self.player.anxiety_afraid is not None and self.player.anxiety_afraid != 1)


class SurveyPage_HSRC_General_4(SurveyPage):
    pass
    # debug_fill_forms_randomly = True


# The following page displays only if at least one problem was indicated on the prior page.
class SurveyPage_HSRC_General_4b(SurveyPage):
    pass
    # debug_fill_forms_randomly = True

    def is_displayed(self):
        return (self.player.depression_pleasure is not None and self.player.depression_pleasure != 1) or \
               (self.player.depression_hopeless is not None and self.player.depression_hopeless != 1) or \
               (self.player.depression_sleep is not None and self.player.depression_sleep != 1) or \
               (self.player.depression_energy is not None and self.player.depression_energy != 1) or \
               (self.player.appetite is not None and self.player.appetite != 1) or \
               (self.player.depression_failure is not None and self.player.depression_failure != 1) or \
               (self.player.depression_concentration is not None and self.player.depression_concentration != 1) or \
               (self.player.depression_movement is not None and self.player.depression_movement != 1) or \
               (self.player.depression_dead is not None and self.player.depression_dead != 1)


survey_pages = [
    SurveyPage_HSRC_General_1,
    SurveyPage_HSRC_USA_1,
    SurveyPage_HSRC_RSA_1,
    SurveyPage_HSRC_General_2,
    SurveyPage_HSRC_General_3,
    SurveyPage_HSRC_General_3b,
    SurveyPage_HSRC_General_4,
    SurveyPage_HSRC_General_4b,
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
