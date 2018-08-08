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
from django import forms
from otreeutils.surveys import create_player_model_for_survey, generate_likert_field, generate_likert_table
from common_helper_functions import set_default_pvars

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'hsrc_survey_task'
    players_per_group = None
    num_rounds = 1
    app_name = 'hsrc_survey_task'


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            set_default_pvars(p)


class Group(BaseGroup):
    pass


def my_generate_likert_table(labels, questions, form_name=None, help_texts=None, widget=None, use_likert_scale=True,
                                make_label_tag=False, **kwargs):
    """
    Generate a table with Likert scales between 1 and `len(labels)` in each row for questions supplied with
    `questions` as list of tuples (field name, field label).
    Optionally provide `help_texts` which is a list of help texts for each question (hence must be of same length
    as `questions`.
    If `make_label_tag` is True, then each label is surrounded by a <label>...</label> tag, otherwise it's not.
    Optionally set `widget` (default is `RadioSelect`).
    """
    if not help_texts:
        help_texts = [''] * len(questions)

    if not widget:
        widget = widgets.RadioSelect

    if len(help_texts) != len(questions):
        raise ValueError('Number of questions must be equal to number of help texts.')

    if use_likert_scale:
        field_generator = generate_likert_field(labels, widget=widget)
        header_labels = labels
    else:
        field_generator = partial(models.StringField, choices=labels, widget=widget or widgets.RadioSelectHorizontal)
        header_labels = [t[1] for t in labels]

    fields = []
    for (field_name, field_label), help_text in zip(questions, help_texts):
        fields.append((field_name, {
            'help_text': help_text,
            'label': field_label,
            'make_label_tag': make_label_tag,
            'field': field_generator(blank=True),
        }))

    form_def = {'form_name': form_name, 'fields': fields, 'render_type': 'table', 'header_labels': header_labels}
    form_def.update(dict(**kwargs))

    return form_def


# Player model is dynamically created below
# class Player(BasePlayer):
#    pass

YESNO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)


YESNO_DONTKNOW_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('do_not_know', "I don't know"),
)

likert_4_labels = (
    'RARELY/NEVER',  # value: 1
    'OCCASIONALLY',  # value: 2
    'OFTEN',  # ...
    'ALMOST ALWAYS',
)

likert_11_labels = (
    '0 - Not At All Willing To Take Risks',  # value: 1
    '1',  # value: 2
    '2',  # ...
    '3',
    '4',  # value: 5
    '5',
    '6',
    '7',
    '8',
    '9',
    '10 - Very Willing To Take Risks',
)

AGREE_DISAGREE_5_CHOICES = (
    ('1_strongly_agree', 'Strongly agree'),
    ('2_agree', 'Agree'),
    ('3_neutral', 'Neutral'),
    ('4_disagree', 'Disagree'),
    ('5_strongly_disagree', 'Strongly disagree'),
)

likert_11point_field = generate_likert_field(likert_11_labels)

COVID_CAUSE_CHOICES = (
    ('bacteria', 'Bacterial infection'),
    ('insect', 'Insect bite'),
    ('virus', 'Viral infection'),
    ('animal', 'Animals'),
    ('do_not_know', "I don't know"),
)

COVID_SPREAD_CHOICES = (
    ('cough', 'Infected persons coughing or sneezing'),
    ('gathering', 'By being in a public gathering where there is an infected person'),
    ('surface', 'Virus-contaminated surfaces'),
    ('face', 'Touching your face after you have been in contact with an infected person'),
    ('do_not_know', "I don't know"),
)

COVID_INCUBATION_CHOICES = (
    ('0 days', 'Immediately'),
    ('1-2 days', 'After 1-2 days'),
    ('2-14 days', 'After 2-14 days'),
    ('15-20 days', 'After 15-20 days'),
    ('do_not_know', "I don't know"),
)

COVID_SYMPTOMS_CHOICES = (
    ('pain', 'Body pain'),
    ('sweating', 'Sweating'),
    ('short_breath', 'Shortness of breath'),
    ('headache', 'Headaches'),
    ('cough', 'Cough'),
    ('runny_nose', 'Running nose'),
    ('sneeze', 'Sneezing'),
    ('red_eyes', 'Red-itchy eyes'),
    ('fever', 'Fever'),
    ('diarrhea', 'Diarrhea'),
    ('do_not_know', "I don't know"),
)

COVID_PREVENTION_CHOICES = (
    ('cover_mouth', 'Covering your mouth with a flexed elbow when coughing'),
    ('gloves', 'Using gloves'),
    ('face_mask', 'Using face mask'),
    ('wash_hands', 'Washing your hands regularly with soap for 20 seconds'),
    ('do_not_know', "I don't know"),
)

COVID_BEHAVIORS_CHOICES = (
    ('cover_mouth', 'Covering coughs or sneezes with a tissue or flexed elbow'),
    ('gloves', 'Wearing hand gloves'),
    ('mask', 'Using face mask'),
    ('hand_sanitizer', 'Using hand sanitizer'),
    ('wash_hands', 'Washing my hands more frequently'),
    ('stay_home', 'Staying in my house and decreasing my social interaction'),
    ('self_isolate', 'Self-isolating'),
    ('no_precautions', "I haven't taken any precautions yet"),
    ('other', 'Other'),
)

COVID_PERSONAL_RISK_CHOICES = (
    ('1_vh', 'Very high risk'),
    ('2_h', 'High risk'),
    ('3_m', 'Moderate risk'),
    ('4_l', 'Low risk'),
    ('5_vl', 'Very low risk'),
)

COVID_PERSONAL_RISK_FACTORS_CHOICES = (
    ('young', 'I am in a young age group'),
    ('medical_condition', 'I have underlying medical conditions'),
    ('wash_hands', 'I wash my hands regularly'),
    ('smoke', 'I smoke'),
    ('high_risk_employment', 'I work in a high-risk environment (hospital, police station, essential services)'),
    ('high_risk_home', 'My home environment places me at risk'),
    ('self_isolate', 'I am self-isolating'),
    ('gloves', 'I am using gloves'),
    ('high_risk_age', 'I am in a high-risk age group'),
    ('healthy', 'I am generally healthy'),
    ('face_mask', 'I use a face mask'),
    ('do_not_know', "I don't know"),
    ('other', 'Other'),
)

COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES = (
    ('higher', 'HIGHER than my personal risk'),
    ('same', 'About the SAME as my personal risk'),
    ('lower', 'LESS than my personal risk'),

)


USA_COVID_INFORMATION_CHOICES = (
    ('local_tv', 'Local television'),
    ('abc', 'ABC'),
    ('cbs', 'CBS'),
    ('nbc', 'NBC'),
    ('pbs', 'PBS'),
    ('fox', 'FOX News'),
    ('cnn', 'CNN'),
    ('msnbc', 'MSNBC'),
    ('i24', 'i24 News'),
    ('newsmax', 'NEWSMAX'),
    ('comedy', 'Late-Night Comedy (Daily Show, Tonight Show, John Oliver etc.)'),
    ('spanish', 'Spanish-language tv'),
    ('radio_non_partisan', 'Non-partisan radio'),
    ('radio_conservative', 'Conservative talk radio'),
    ('radio_liberal', 'Liberal talk radio'),
    ('newspaper_national', 'US Newspapers (print or online)'),
    ('newspaper_international', 'International Newspapers (includes The Economist)'),
    ('social_media', 'Social media'),
    ('news_website', 'News websites or mobile apps'),
    ('government', 'Government sources'),
    ('spouse_child', 'Spouse or children'),
    ('doctor', 'Personal doctor'),
    ('friend', 'Friends'),
    ('family', 'Family'),
    ('journal', 'Scientific journals'),
    ('do_not_know', "I don't know"),
    ('other', 'Other'),
)

COVID_ONE_MONTH_CHOICES = (
    ('better', 'We will be over the worst of it - things will begin to improve'),
    ('same', 'The situation will remain largely the same as it is now'),
    ('worse', 'The worst is yet to come - things will start to get worse'),
    ('do_not_know', "I don't know"),
)

COVID_PEAK_CHOICES = (
    ('before', 'Before'),
    ('same', 'At the same time'),
    ('after', 'After'),
    ('do_not_know', 'don’t know'),
)

RSA_COVID_INFORMATION_CHOICES = (
    ('local_tv', 'Local television'),
    ('sat_tv_national', 'Satellite television: South African stations'),
    ('sat_tv_international', 'Satellite television: International stations (CNN, Al Jazeera, etc.)'),
    ('radio', 'Radio'),
    ('newspaper_national', 'South African newspapers (print or online)'),
    ('newspaper_international', 'International newspapers (includes The Economist)'),
    ('social_media', 'Social media'),
    ('news_website', 'News websites or mobile apps'),
    ('government', 'Government sources'),
    ('spouse_child', 'Spouse or children'),
    ('doctor', 'Personal doctor'),
    ('friend', 'Friends'),
    ('family', 'Family'),
    ('journal', 'Scientific journals'),
    ('do_not_know', "I don't know"),
    ('other', 'Other'),
)

COVID_DURATION_CHOICES = (
    ('few_days', 'Few days'),
    ('few_weeks', 'Few weeks'),
    ('few_months', 'Few months'),
    ('at_least_12_months', 'Will last at least 12 months'),
    ('do_not_know', "I don't know"),
)

COVID_VACCINE_CHOICES = (
    ('6_months', 'The next 6 months'),
    ('12_months', 'Within one year'),
    ('18_months', 'Within 18 months'),
    ('at_least_18_months', 'After the next 12 to 18 months'),
    ('do_not_know', "I don't know"),
)

COVID_DIMINISH_INCOME_CHOICES = (
    ('yes_alot', 'Yes, a lot'),
    ('yes_alittle', 'Yes, a little'),
    ('no', 'No'),
)

COVID_TEST_POSITIVE_RELATIONSHIP_CHOICES = (
    ('na', 'Not applicable'),
    ('family', 'Family'),
    ('friend', 'Friend'),
    ('neighbor', 'Neighbor'),
    ('work', 'People at work'),
    ('child', 'Child'),
    ('partner', 'Partner'),
)

COVID_TEST_POSITIVE_RELATIONSHIP_CHOICES = (
    ('na', 'Not applicable'),
    ('family', 'Family'),
    ('friend', 'Friend'),
    ('neighbor', 'Neighbor'),
    ('work', 'People at work'),
    ('child', 'Child'),
    ('partner', 'Partner'),
)

COVID_EXPOSED_ACTIONS_CHOICES = (
    ('isolate', 'Isolate myself'),
    ('hotline', 'Call the COVID-19 hotline'),
    ('doctor', 'Contact my personal doctor'),
    ('hospital', 'Go to the hospital emergency department'),
    ('social_media', 'Post the news to my social media'),
    ('employer', 'Alert my employer'),
    ('flu', 'Treat it like I would any flu'),
    ('do_not_know', "I don't know"),
    ('other', 'Other'),
)

ANXIETY_DEPRESSION_CHOICES = (
    ('0', 'Not At All'),
    ('1', 'Several Days'),
    ('2', 'More Than Half the Days'),
    ('3', 'Most of the Days'),
)

ANXIETY_DEPRESSION_DIFFICULTY_CHOICES = (
    # ('na', 'I did not check off any problems above'),
    ('not_difficult', 'Not difficult at all'),
    ('somewhat_difficult', 'Somewhat difficult'),
    ('very_difficult', 'Very difficult'),
    ('extremely_difficult', 'Extremely difficult'),
)

ANXIETY_DEPRESSION_LIKERT_CHOICES = (
    'Not At All',               # value: 1
    'Several Days',             # value: 2
    'More Than Half the Days',  # value: 3
    'Most of the Days',         # value: 4
)

LIKERT_7_NOTATALL_COMPLETELY_CHOICES = (
    '1 - Not at all',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7 - Completely',
)

likert_7_notatall_completely_field = generate_likert_field(LIKERT_7_NOTATALL_COMPLETELY_CHOICES)

LIKERT_7_VERYLOW_VERYHIGH_CHOICES = (
    '1 - Very low',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7 - Very high',
)

likert_7_verylow_veryhigh_field = generate_likert_field(LIKERT_7_VERYLOW_VERYHIGH_CHOICES)

# make sure to use a tuple instead of a list here, otherwise oTree will complain:
SURVEY_DEFINITIONS = (
    {
        # HSRC general p1
        'page_title': 'Health Questionnaire',
        'survey_fields': [
            ('covid_cause', {
                'text': 'COVID-19 is caused by:',
                'field': models.CharField(blank=True, choices=COVID_CAUSE_CHOICES),
            }),
            ('covid_spread', {
                'text': 'COVID-19 is spread by direct contact with the virus from:'
                        '<br>(select all that apply)',
                'field':  models.CharField(blank=True,
                                           widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_SPREAD_CHOICES)),
            }),
            ('covid_incubation', {
                'text': 'What is the average length of time between a person’s becoming infected with COVID-19 and '
                        'experiencing symptoms (taking into account that some people become infected and never show '
                        'symptoms)? ',
                'field': models.CharField(blank=True, choices=COVID_INCUBATION_CHOICES),
            }),
            ('covid_symptoms', {
                'text': 'Which of the following best describes the symptoms of COVID-19?'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_SYMPTOMS_CHOICES)),
            }),
            ('covid_prevention', {
                'text': 'Prevention of COVID-19 infection is best achieved by:'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_PREVENTION_CHOICES)),
            }),
            ('covid_behaviors', {
                'text': 'Have you been doing any of the following during the past week as a result of the COVID-19 '
                        'emergency? '
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_BEHAVIORS_CHOICES)),
            }),
        ]
    },
    {
        # HSRC USA p1
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            ('usa_covid_personal_risk', {
                'text': 'How do you rate your PERSONAL RISK of contracting COVID-19? ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_CHOICES),
            }),
            ('usa_covid_personal_risk_factors', {
                'text': 'Why do you believe that you are at the PERSONAL LEVEL of risk you indicated above?'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_PERSONAL_RISK_FACTORS_CHOICES)),
            }),
            ('usa_covid_personal_risk_world', {
                'text': 'Do you feel the level of risk in contracting COVID-19 for each of the following is HIGHER or '
                        'LOWER than your PERSONAL LEVEL of risk indicated above?'
                        '<br><br>'
                        'The world: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('usa_covid_personal_risk_usa', {
                'text': 'The United States: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('usa_covid_personal_risk_state', {
                'text': 'My State: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('usa_covid_personal_risk_neighborhood', {
                'text': 'My Neighborhood: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('usa_covid_personal_risk_family', {
                'text': 'My Family: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),

            ('usa_experts_confidence', {
                'help_text': """
                        <p>On the 7-point scale below, where 1 means "not at all" and 7 means "completely", how
                        confident are you that the estimates of COVID-19 cases and deaths published on a rolling basis
                        by the US Center for Disease Control (CDC) tend to accurately reflect reality?</p>
                    """,
                'field': likert_7_notatall_completely_field(blank=True),  # don't forget the parentheses at the end!
                'widget_attrs': {},
            }),
            ('usa_covid_information', {
                'text': 'Where do you get most of your information on COVID-19?'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=USA_COVID_INFORMATION_CHOICES)),
            }),
            ('usa_information_confidence', {
                'help_text': """
                    <p>On the 7-point scale below, where 1 means "very low" and 7 means "very high", what level of
                    confidence do you have in the general accuracy of reporting about COVID-19 you get from the
                    information source that you consult most often when you want to find about the current course of
                    the disease?</p>
                """,
                'field': likert_7_verylow_veryhigh_field(blank=True),
                'widget_attrs': {},
            }),

            ('usa_covid_one_month', {
                'text': 'When thinking about COVID-19 here in the United States, which of the following do you think '
                        'is most likely to happen over the next month?',
                'field': models.CharField(blank=True, choices=COVID_ONE_MONTH_CHOICES),
            }),
            ('usa_covid_peak_atlanta', {
                'text': 'Will the Atlanta metropolitan area reach its peak rate of COVID-19 infection before or after '
                        'the United States reaches its peak rate?',
                'field': models.CharField(blank=True, choices=COVID_PEAK_CHOICES),
            }),
        ]
    },
    {
        # HSRC RSA p1
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            ('rsa_covid_personal_risk', {
                'text': 'How do you rate your PERSONAL RISK of contracting COVID-19? ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_CHOICES),
            }),
            ('rsa_covid_personal_risk_factors', {
                'text': 'Why do you believe that you are at the PERSONAL LEVEL of risk you indicated above?'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_PERSONAL_RISK_FACTORS_CHOICES)),
            }),
            ('rsa_covid_personal_risk_world', {
                'text': 'Do you feel the level of risk in contracting COVID-19 for each of the following is HIGHER or '
                        'LOWER than your PERSONAL LEVEL of risk indicated above?'
                        '<br><br>'
                        'The world: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('rsa_covid_personal_risk_rsa', {
                'text': 'South Africa: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('rsa_covid_personal_risk_state', {
                'text': 'My Province: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('rsa_covid_personal_risk_neighborhood', {
                'text': 'My Neighborhood: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),
            ('rsa_covid_personal_risk_family', {
                'text': 'My Family: ',
                'field': models.CharField(blank=True, choices=COVID_PERSONAL_RISK_HIGH_SAME_LOW_CHOICES),
                'widget_attrs': {'style': 'display:inline'},
            }),

            ('rsa_experts_confidence', {
                'help_text': """
                    <p>On the 7-point scale below, where 1 means "not at all" and 7 means "completely", how confident
                    are you that the estimates of COVID-19 cases and deaths published on a rolling
                    basis by the South African Department of Health tend to accurately reflect reality?</p>
                """,
                'field': likert_7_notatall_completely_field(blank=True),
                'widget_attrs': {},
            }),
            ('rsa_covid_information', {
                'text': 'Where do you get most of your information on COVID-19?'
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=RSA_COVID_INFORMATION_CHOICES)),
            }),
            ('rsa_information_confidence', {
                'help_text': """
                    <p>On the 7-point scale below, where 1 means "very low" and 7 means "very high", what level of
                    confidence do you have in the general accuracy of reporting about COVID-19 you get from the
                    information source that you consult most often when you want to find about the current course of
                    the disease?</p>
                """,
                'field': likert_7_verylow_veryhigh_field(blank=True),
                'widget_attrs': {},
            }),

            ('rsa_covid_one_month', {
                'text': 'When thinking about COVID-19 here in South Africa, which of the following do you think is '
                        'most likely to happen over the next month?',
                'field': models.CharField(blank=True, choices=COVID_ONE_MONTH_CHOICES),
            }),
            ('rsa_covid_peak_capetown', {
                'text': 'Will the Cape Town metropolitan area reach its peak rate of COVID-19 infection before or '
                        'after South Africa reaches its peak rate?',
                'field': models.CharField(blank=True, choices=COVID_PEAK_CHOICES),
            }),
        ]
    },
    {
        # HSRC general p2
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            ('covid_media_exaggerated', {
                'text': 'I believe the threat from COVID-19 is exaggerated in the media on which I mainly rely for '
                        'news:',
                'field': models.CharField(blank=True, choices=AGREE_DISAGREE_5_CHOICES),
            }),
            ('covid_media_overload', {
                'text': "I feel there is far too much information in the media on which I mainly rely for news, "
                        "and I can't keep up with it all:",
                'field': models.CharField(blank=True, choices=AGREE_DISAGREE_5_CHOICES),
            }),
            ('covid_duration', {
                'text': 'This whole COVID-19 crisis will be over in the next:',
                'field': models.CharField(blank=True, choices=COVID_DURATION_CHOICES),
            }),
            ('covid_medication', {
                'text': 'Is there currently a medication to treat COVID-19?',
                'field': models.CharField(blank=True, choices=YESNO_DONTKNOW_CHOICES),
            }),
            ('covid_cure', {
                'text': 'Is there currently a cure for COVID-19?',
                'field': models.CharField(blank=True, choices=YESNO_DONTKNOW_CHOICES),
            }),
            ('covid_vaccine', {
                'text': 'Governments and pharmaceutical companies will develop a vaccine within:',
                'field': models.CharField(blank=True, choices=COVID_VACCINE_CHOICES),
            }),
            ('covid_diminish_income', {
                'text': 'If you are required to stay quarantined at home, does this affect your income?',
                'field': models.CharField(blank=True, choices=COVID_DIMINISH_INCOME_CHOICES),
            }),
            ('covid_test_positive', {
                'text': 'Do you personally know anyone who has tested positive for COVID-19?',
                'field': models.CharField(blank=True, choices=YESNO_CHOICES),
            }),
            ('covid_test_positive_relationship', {
                'text': 'If you do know someone that tested positive for COVID-19, what is your relationship to those '
                        'individuals? '
                        '<br>(select all that apply)',
                'field':  models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_TEST_POSITIVE_RELATIONSHIP_CHOICES)),
            }),
            ('covid_test_self', {
                'text': 'Have you been tested for COVID-19?',
                'field': models.CharField(blank=True, choices=YESNO_CHOICES),
            }),
            ('covid_exposed_actions', {
                'text': 'If you do start showing symptoms and you suspect you may have been exposed to COVID-19, '
                        'what would be your immediate course of action? '
                        '<br>(select all that apply)',
                'field': models.CharField(blank=True,
                    widget=forms.widgets.CheckboxSelectMultiple(choices=COVID_EXPOSED_ACTIONS_CHOICES)),
            }),
            ('covid_int_travel_30days', {
                'text': 'Have you traveled out of the country in the last 30 days? ',
                'field': models.CharField(blank=True, choices=YESNO_CHOICES),
            }),
        ]
    },
    {
        # HSRC general p3
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            my_generate_likert_table(ANXIETY_DEPRESSION_LIKERT_CHOICES, [
                ('anxiety_nervous', 'Feeling nervous, anxious, or on edge'),
                ('anxiety_worry_uncontrolled', 'Not being able to stop or control worrying'),
                ('anxiety_worry_multiple', 'Worrying too much about different things'),
                ('anxiety_relax', 'Trouble relaxing'),
                ('anxiety_restless', "Being so restless that it's hard to sit still"),
                ('anxiety_irritable', 'Becoming easily annoyed or irritable'),
                ('anxiety_afraid', 'Feeling afraid as if something awful might happen'),
            ],
                                  form_help_initial='<p>Over the last 2 weeks, how often have you been bothered by '
                                                    'the following problems?</p>',
                                  table_repeat_header_each_n_rows=10,
                                  table_rows_equal_height=False
                                  )
        ]
    },
    {
        # HSRC general p3b (shown conditionally based on is_displayed() in pages.py)
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            ('anxiety_difficulty', {
                'text': 'Considering the problems you indicated on the previous page, how difficult have these '
                        'problems made it for you to do your work, take care of things at home, or get along with '
                        'other people?',
                'field': models.CharField(blank=True, choices=ANXIETY_DEPRESSION_DIFFICULTY_CHOICES),
            }),
        ]
    },
    {
        # HSRC general p4
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            my_generate_likert_table(ANXIETY_DEPRESSION_LIKERT_CHOICES, [
                ('depression_pleasure', 'Little interest or pleasure in doing things'),
                ('depression_hopeless', 'Feeling down, depressed, or hopeless'),
                ('depression_sleep', 'Trouble falling or staying asleep, or sleeping too much'),
                ('depression_energy', 'Feeling tired or having little energy'),
                ('appetite', 'Poor appetite or overeating'),
                ('depression_failure',
                 'Feeling bad about yourself or that you are a failure or have let yourself or your family down'),
                ('depression_concentration',
                 'Trouble concentrating on things, such as reading the newspaper or watching television'),
                ('depression_movement',
                 'Moving or speaking so slowly that other people could have noticed. Or the opposite being so fidgety '
                 'or restless that you have been moving around a lot more than usual'),
                ('depression_dead', 'Thoughts that you would be better off dead, or of hurting yourself'),
            ],
                                  form_help_initial='<p>Over the last 2 weeks, how often have you been bothered by '
                                                    'the following problems?.</p>',
                                  table_repeat_header_each_n_rows=10,
                                  table_rows_equal_height=False
                                  )
        ]
    },
    {
        # HSRC general p4b (shown conditionally based on is_displayed() in pages.py)
        'page_title': 'Health Questionnaire (continued)',
        'survey_fields': [
            ('depression_difficulty', {
                'text': 'Considering the problems you indicated on the previous page, how difficult have these '
                        'problems made it for you to do your work, take care of things at home, or get along with '
                        'other people?',
                'field': models.CharField(blank=True, choices=ANXIETY_DEPRESSION_DIFFICULTY_CHOICES),
            }),
        ]
    },

    # ... more pages
)


Player = create_player_model_for_survey('hsrc_survey_task.models', SURVEY_DEFINITIONS)
