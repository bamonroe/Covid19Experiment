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
    name_in_url = 'demog_survey_task'
    players_per_group = None
    num_rounds = 1
    app_name = 'demog_survey_task'


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


AGE_CHOICES = (
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
)

GENDER_CHOICES = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('other', 'Other'),
    ('no_answer', 'Prefer not to answer'),
)

USA_RACE_CHOICES = (
    ('white', 'White or Caucasian'),
    ('black', 'Black or African American'),
    ('african', 'African'),
    ('asian-american', 'Asian-American'),
    ('asian', 'Asian'),
    ('hispanic-american', 'Hispanic-American'),
    ('hispanic', 'Hispanic'),
    ('mixed', 'Mixed-race / Multiracial'),
    ('hawaiian', 'Native Hawaiian or other Pacific Islander'),
    ('other', 'Other'),
)

RSA_RACE_CHOICES = (
    ('black_african', 'Black / African'),
    ('coloured', 'Coloured'),
    ('asian_indian', 'Asian / Indian'),
    ('white', 'White'),
    ('no_answer', 'Prefer not to answer'),
    ('other', 'Other'),
)

USA_MAJOR_CHOICES = (
    ('acct', 'Accounting'),
    ('bio', 'Biological Sciences'),
    ('econ', 'Economics'),
    ('math', 'Math, Computer Sciences, or Physical Sciences'),
    ('fin', 'Finance'),
    ('soc', 'Social Sciences or History'),
    ('busadmin', 'Business Administration, other than Accounting, Economics, or Finance'),
    ('hum', 'Humanities'),
    ('educ', 'Education'),
    ('psych', 'Psychology'),
    ('eng', 'Engineering'),
    ('health', 'Health Professions'),
    ('pubaffairs', 'Public Affairs or Social Services'),
    ('na', 'Does not apply'),
    ('other', 'Other'),
)

USA_CLASS_CHOICES = (
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
    ('Masters', 'Masters'),
    ('Doctoral', 'Doctoral'),
    ('na', 'Does not apply'),
    ('other', 'Other'),
)

USA_EXPECTED_EDUCATION_CHOICES = (
    ('assoc', "Associate's degree"),
    ('bach', "Bachelor's degree"),
    ('mast', "Master's degree"),
    ('doc', 'Doctoral degree'),
    ('prof', 'First professional degree'),
)

USA_PARENT_EDUCATION_CHOICES = (
    ('less_than_hs', 'Less than High School'),
    ('ged', 'GED or High School Equivalency'),
    ('hs', 'High School'),
    ('voc', 'Vocational or Trade School'),
    ('uni', 'College or University'),
    ('do_not_know', "Don't know"),
    ('na', 'Not applicable'),
)

USA_GPA_CHOICES = (
    ('a', "Between 3.75 and 4.0 GPA (mostly A's)"),
    ('ab', "Between 3.25 and 3.74 GPA (about half A's and half B's)"),
    ('b', "Between 2.75 and 3.24 GPA (mostly B's)"),
    ('bc', "Between 2.25 and 2.74 GPA (about half B's and half C's)"),
    ('c', "Between 1.75 and 2.24 GPA (mostly C's)"),
    ('cd', "Between 1.25 and 1.74 GPA (about half C's and half D's)"),
    ('d', "Less than 1.25 GPA (mostly D's or below)"),
    ('na', 'Have not taken courses for which grades are given'),
)

RELATIONSHIP_CHOICES = (
    ('single', 'Single and never married'),
    ('in_relationship', 'In a relationship, but not married'),
    ('married', 'Married'),
    ('separated', 'Separated, divorced, or widowed'),
    ('other', 'Other'),
)

USA_RESIDE_CHOICES = (
    ('own', 'Your own place (apartment, house, condo, etc.)'),
    ('parent', "Parent or Guardian's home"),
    ('another', "Another's home (non-parental relative's or non-related adult's home)"),
    ('group', 'Group living arrangement (dormitory, barracks, group home, etc.)'),
    ('homeless', 'Homeless (no regular place to stay)'),
    ('other', 'Other'),
)

USA_RESIDE_HOME_TYPE_CHOICES = (
    ('stand_alone', 'Stand Alone House'),
    ('semi_detached', 'Town House or Semi-Detached House'),
    ('multi_unit', 'Apartment or Condo in Multi-Unit Building'),
)

RSA_HOME_TYPE_CHOICES = (
    ('house', 'Stand Alone House'),
    ('townhouse', 'Town House / Semi Detached House'),
    ('flat', 'Flat in Block of Flats'),
    ('hut', 'Traditional Dwelling / Hut'),
    ('house_room_backyard', 'House / Room in Back Yard'),
    ('shack_backyard', 'Shack in Back Yard'),
    ('informal', 'Informal Dwelling / Shack Not in Back Yard'),
    ('tent', 'Tent / Caravan'),
)



FINANCIAL_SITUATION_CHOICES = (
    (1, 'Very broke'),
    (2, 'Broke'),
    (3, 'Neither broke nor in good shape'),
    (4, 'In good shape'),
    (5, 'In very good shape'),
)

HOUSEHOLD_MEMBERS_CHOICES = (
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
)

USA_INCOME_CHOICES = (
    ('<15k', '$15,000 or under'),
    ('15k-25k', '$15,001 - $25,000'),
    ('25k-35k', '$25,001 - $35,000'),
    ('35k-50k', '$35,001 - $50,000'),
    ('50k-65k', '$50,001 - $65,000'),
    ('65k-80k', '$65,001 - $80,000'),
    ('80k-100k', '$80,001 - $100,000'),
    ('100k-150k', '$100,001 - $150,000'),
    ('>150k', 'Over $150,000'),
    ('do_not_know', "Don't know"),
    ('prefer_to_not_answer', 'Prefer to not answer'),
)

EMPLOYMENT_CHOICES = (
    ('full_time', 'Employed - Full Time (Fixed Salary Per Month)'),
    ('part_time', 'Employed - Informal Sector / Part Time (Non-Fixed Salary Per Month)'),
    ('unemployed_looking', 'Unemployed and currently looking for work'),
    ('unemployed_not_looking', 'Unemployed and NOT currently looking for work'),
    ('home', 'Home Duties'),
    ('student', 'Full-Time Student'),
    ('retired', 'Retired'),
    ('self_employed', 'Self Employed'),
    ('cant_work', 'Unable to work'),
)

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

USA_RELIGION_CHOICES = (
    ('atheism', 'Atheism'),
    ('buddhism', 'Buddhism'),
    ('christ-bapt', 'Christianity - Baptist'),
    ('christ-cath', 'Christianity - Catholic'),
    ('christ-luth', 'Christianity - Lutheran'),
    ('christ-meth', 'Christianity - Methodist'),
    ('christ-other', 'Christianity - Other'),
    ('hinduism', 'Hinduism'),
    ('islam', 'Islam'),
    ('judaism', 'Judaism'),
    ('agnostic', 'Nonreligious or Agnostic'),
    ('blank', 'Prefer to not answer'),
    ('other', 'Other'),
)


# make sure to use a tuple instead of a list here, otherwise oTree will complain:
SURVEY_DEFINITIONS = (
    {
        # General page
        'page_title': 'Survey Questions',
        'survey_fields': [
            ('age', {
                'text': 'What is your current age?',
                'field': models.IntegerField(blank=True, choices=AGE_CHOICES),
            }),
            ('gender', {
                'text': 'Which of the following gender groups do you identify with?',
                'field': models.CharField(blank=True, choices=GENDER_CHOICES),
            }),
            ('location', {
                'text': 'Where are you currently taking part in this survey? That is, what CITY and STATE/PROVINCE '
                        'are you currently in?',
                'field': models.CharField(blank=True, max_length=200),
            }),
            ('relationship', {
                'text': 'What relationship status describes you currently?',
                'field': models.CharField(blank=True, choices=RELATIONSHIP_CHOICES),
            }),
            ('income_last_month', {
                'text': 'In the last month, what was your total income from all sources?',
                'field': models.CharField(blank=True, max_length=200),
            }),
            ('income_day_received', {
                'text': 'On what day do you typically receive your income each month?',
                'field': models.CharField(blank=True, max_length=200),
            }),
            ('expenditure_daily', {
                'text': 'How much do you typically spend each day using cash and your debit card?',
                'field': models.CharField(blank=True, max_length=200),
            }),
            ('financial_situation', {
                'text': "What is your current (TODAY's) financial situation on the following scale?",
                'field': models.IntegerField(blank=True, choices=FINANCIAL_SITUATION_CHOICES),
            }),
        ]
    },
    {
        # USA-specific page
        'page_title': 'Survey Questions (continued)',
        'survey_fields': [
            ('usa_race', {
                'text': 'Which of the following categories best describes you?',
                'field': models.CharField(blank=True, choices=USA_RACE_CHOICES),
            }),
            ('usa_race_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_usa_race").val() === "other"'
            }),
            ('usa_major', {
                'text': 'What is your major?',
                'field': models.CharField(blank=True, choices=USA_MAJOR_CHOICES),
            }),
            ('usa_major_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_usa_major").val() === "other"'
            }),
            ('usa_class_standing', {
                'text': 'What is your class standing?',
                'field': models.CharField(blank=True, choices=USA_CLASS_CHOICES),
            }),
            ('usa_class_standing_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style

                'condition_javascript': '$("#id_usa_class_standing").val() === "other"'
            }),
            ('usa_expected_education', {
                'text': 'What is the highest level of education you expect to complete?',
                'field': models.CharField(blank=True, choices=USA_EXPECTED_EDUCATION_CHOICES),
            }),
            ('usa_father_education', {
                'text': 'What was the highest level of education that your father (or male guardian) completed?',
                'field': models.CharField(blank=True, choices=USA_PARENT_EDUCATION_CHOICES),
            }),
            ('usa_mother_education', {
                'text': 'What was the highest level of education that your mother (or female guardian) completed?',
                'field': models.CharField(blank=True, choices=USA_PARENT_EDUCATION_CHOICES),
            }),
            ('usa_gpa', {
                'text': 'On a 4-point scale, what is your current GPA if you are doing a Bachelors degree, '
                        'or what was it when you did a Bachelors degree? This GPA should refer to all of your '
                        'coursework, not just the current year.',
                'field': models.CharField(blank=True, choices=USA_GPA_CHOICES),
            }),
            ('usa_reside', {
                'text': 'Where do you live now? That is, where do you stay most often?',
                'field': models.CharField(blank=True, choices=USA_RESIDE_CHOICES),
            }),
            ('usa_reside_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_usa_reside").val() === "other"'
            }),
            ('usa_reside_home_type', {
                'text': 'Which of the following best describes your home?',
                'field': models.CharField(choices=USA_RESIDE_HOME_TYPE_CHOICES, blank=True),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_usa_reside").val() === "own" || '
                                        '$("#id_usa_reside").val() === "parent" || '
                                        '$("#id_usa_reside").val() === "another"'
            }),
        ]
    },
    {
        # RSA-specific page
        'page_title': 'Survey Questions (continued)',
        'survey_fields': [
            ('rsa_race', {
                'text': 'In what population group do you classify yourself?',
                'field': models.CharField(blank=True, choices=RSA_RACE_CHOICES),
            }),
            ('rsa_race_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_rsa_race").val() === "other"'
            }),
            ('rsa_home_type', {
                'text': 'Which of the following best describes your home?',
                'field': models.CharField(blank=True, choices=RSA_HOME_TYPE_CHOICES),
            }),
            ('rsa_household_members', {
                'text': 'How many people live in your household? Include yourself, your spouse, and any dependents. '
                        'Do not include your parents or roommates unless you claim them as dependents. (regardless of '
                        'your living situation, always include yourself as "1")',
                'field': models.IntegerField(blank=True, choices=HOUSEHOLD_MEMBERS_CHOICES),
            }),
        ]
    },
    {
        # USA page
        'page_title': 'Survey Questions (continued)',
        'survey_fields': [
            ('usa_household_members', {
                'text': 'How many people live in your household? Include yourself, your spouse, and any dependents. '
                        'Do not include your parents or roommates unless you claim them as dependents (regardless of '
                        'your living situation, always include yourself as "1").',
                'field': models.IntegerField(blank=True, choices=HOUSEHOLD_MEMBERS_CHOICES),
            }),
            ('usa_household_income', {
                'text': 'Please select the category below that best describes the total amount of INCOME earned last '
                        'year by the people in YOUR HOUSEHOLD (as "household" is defined in the previous question). '
                        'Consider all forms of income, including: salaries, tips, interest and dividend payments, '
                        'scholarship support, student loans, parental support, social security, alimony, '
                        'child support, and others.',
                'field': models.CharField(blank=True, choices=USA_INCOME_CHOICES),
            }),
            ('usa_parent_income', {
                'text': 'Please select the category below that best describes the total amount of INCOME earned last '
                        'year by YOUR PARENTS or GUARDIANS. Again, consider all forms of income, including: salaries, '
                        'tips, interest and dividend payments, scholarship support, student loans, parental support, '
                        'social security, alimony, child support, and others.',
                'field': models.CharField(blank=True, choices=USA_INCOME_CHOICES),
            }),
            ('usa_religion', {
                'text': 'How would you characterize your religious beliefs? Please select the option that best '
                        'describes your beliefs.',
                'field': models.CharField(blank=True, choices=USA_RELIGION_CHOICES),
            }),
            ('usa_religion_other', {
                'text': 'please specify (optional)',
                'field': models.CharField(blank=True, max_length=200),
                'widget_attrs': {'style': 'display:inline'},  # adjust widget style
                'condition_javascript': '$("#id_usa_religion").val() === "other"'
            }),
        ]
    },
    {
        # general page
        'page_title': 'Survey Questions (continued)',
        'survey_fields': [
            ('employment', {
                'text': 'What is your current employment status?',
                'field': models.CharField(blank=True, choices=EMPLOYMENT_CHOICES),
            }),
            ('hyp_risk', {  # most of the time, you'd add a "help_text" for a Likert scale question. You can use HTML:
                'help_text': """
                                    <p>How do you see yourself: are you a person who is fully prepared to take risks
                                    or do your try to avoid taking risks? Please select an option on the scale,
                                    where 0 means "not at all willing to take risks" and 10 means "very willing to
                                    take risks". </p>
                                """,
                'field': likert_11point_field(blank=True),   # don't forget the parentheses at the end!
                'widget_attrs': {},
            }),

        ]
    },
    {
        # general page
        'page_title': 'Survey Questions (continued)',
        'survey_fields': [
            my_generate_likert_table(likert_4_labels, [
                ('likert_q01', 'I plan tasks carefully'),
                ('likert_q02', 'I do things without thinking'),
                ('likert_q03', 'I make up my mind quickly (I decide what to do quickly)'),
                ('likert_q04', 'I am happy-go-lucky (I am easy going. I am carefree)'),
                ('likert_q05', 'I don’t “pay attention”'),
                ('likert_q06',
                 'I have “racing” thoughts (I have quickly changing thoughts that I can’t stop or control)'),
                ('likert_q07',
                 'I plan trips well ahead of time (trips doesn’t only mean holidays, or long-distance journeys)'),
                ('likert_q08', 'I am self-controlled'),
                ('likert_q09', 'I concentrate easily'),
                ('likert_q10', 'I save regularly'),
                ('likert_q11',
                 'I “squirm” at speeches or meetings (I have trouble keeping still at speeches or meetings)'),
                ('likert_q12', 'I think carefully about things'),
                ('likert_q13',
                 'I plan for job security (I think about what I need to do to make sure I am employed or have an '
                 'income in the future)'),
                ('likert_q14', 'I say things without thinking'),
                ('likert_q15', 'I like to think about complex problems'),
                ('likert_q16', 'I decide to change jobs (this means leaving a job, not losing it)'),
                ('likert_q17', 'I act “on impulse”'),
                ('likert_q18',
                 'I get easily bored when solving thought problems (I get easily bored when working on games of '
                 'thought like riddles and number games)'),
                ('likert_q19', 'I act on the spur of the moment (I act without thinking)'),
                ('likert_q20', 'I am a steady thinker (I can think about one thing without getting distracted)'),
                ('likert_q21', 'I decide to change where I live'),
                ('likert_q22', 'I buy things on impulse'),
                ('likert_q23', 'I can only think about one problem at a time'),
                ('likert_q24', 'I change hobbies (hobbies include sports and other recreational activities)'),
                ('likert_q25', 'I spend or buy more on credit than I earn'),
                ('likert_q26',
                 'I have outside thoughts when thinking (I have distracting or unintended thoughts when I’m trying to '
                 'think about something else)'),
                ('likert_q27',
                 'I am more interested in the present than the future (I am more concerned about the present than the '
                 'future)'),
                ('likert_q28', 'I am restless at talks or in church'),
                ('likert_q29',
                 'I like puzzles (I like games and tasks that require thinking about one thing for some time)'),
                ('likert_q30', 'I plan for the future'),
            ],
                                  form_help_initial='<p>Please read through the following list of statements. '
                                                    'For each statement, click the box that best describes you.</p>',
                                  table_repeat_header_each_n_rows=10,
                                  table_rows_equal_height=False,
                                  )
        ]
    },

    # ... more pages
)


Player = create_player_model_for_survey('demog_survey_task.models', SURVEY_DEFINITIONS)
