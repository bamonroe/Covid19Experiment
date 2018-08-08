from enum import Enum


def task_sequence_table_info(s, current_app):
    # Create the roadmap list that will display a list of tasks to the subject
    seq = list.copy(s.session.config['app_sequence'])

    # Specify list of apps we will not display to subjects
    hidden_apps = ['intro']

    # Display complete/incomplete status of only *non-hidden* apps to subject

    # Determine current app position in sequence
    # This value is also the count of completed apps
    current_app_position = seq.index(current_app)

    # Determine the most recently-completed *non-hidden* app
    last_completed_visible_app = ''
    for i in range(current_app_position - 1, -1, -1):
        if seq[i] not in hidden_apps:
            last_completed_visible_app = seq[i]
            break

    # Remove the apps we do not want to display to subject
    seq = [a for a in seq if a not in hidden_apps]

    # Get number of completed tasks in list modified for display
    try:
        num_displayed_apps_completed = seq.index(last_completed_visible_app) + 1
    except ValueError:
        num_displayed_apps_completed = -1

    # Create a helper list for numbering just the incentivized tasks
    incentives_seq = list.copy(seq)
    try:
        incentives_seq.remove('demog_survey_task')
    except ValueError:
        pass
    try:
        incentives_seq.remove('hsrc_survey_task')
    except ValueError:
        pass

    # Rename each app with a friendly name
    rename_seq = {
            "demog_survey_task" : "Survey Questions",
            "hsrc_survey_task"  : "Health Questionnaire",
            "final_page"        : "Final Earnings After Completion",
            }

    seq = [rename_seq[s] if s in rename_seq else s for s in seq]

    for i in range(len(incentives_seq)):
        seq[:] = ['Task ' + str(i+1) if s == incentives_seq[i] else s for s in seq]

    d = {
        "sequence" : seq,
        "num_tasks_completed" : num_displayed_apps_completed
        }

    return d


def get_expiration_time(s):
    if "end_time" in s.participant.vars:
        from datetime import datetime
        exp_time = datetime.timestamp(s.participant.vars['end_time'])
    else:
        exp_time = -1
    return exp_time


def set_default_pvars(p):
    if "locale" not in p.participant.vars:
        p.participant.vars["locale"] = "usa"
    if "treatment" not in p.participant.vars:
        p.participant.vars["treatment"] = 1
    if "wave" not in p.participant.vars:
        p.participant.vars["wave"] = 1
    if "endowment" not in p.participant.vars:
        p.participant.vars["endowment"] = 7
    if "start_time" not in p.participant.vars:
        import datetime
        start_dtime = datetime.datetime.utcnow()
        p.participant.vars["start_time"] = start_dtime
    if "end_time" not in p.participant.vars:
        import datetime
        end_dtime = datetime.datetime.utcnow() + datetime.timedelta(hours = 1)
        p.participant.vars["end_time"] = end_dtime
    if p.participant.label == None:
        p.participant.label == "testsubject"


def format_datetime(x):
    # This function formats a UTC datetime for display to subject, the locale-specific formatting includes:
    # 1. converting to appropriate timezone;
    # 2. formatting hours to be either 12/24 hours
    # 3. displaying am/pm for 12 hour format

    from dateutil import tz

    locale = x.participant.vars["locale"]

    rsa_time_format = "%H:%M "
    usa_time_format = "%I:%M %p "
    if locale == "rsa":
        ampm = ""
        if x.participant.vars["end_time"].astimezone(tz.gettz("Africa/Johannesburg")).hour >= 12:
            ampm = "PM "
        else:
            ampm = "AM "
        date_display_format = ampm + "in South Africa on %A, %B %d, %Y"
    else:
        date_display_format = "in Atlanta, Georgia on %A, %B %d, %Y"

    if locale == "rsa":
        datetime_display_format = rsa_time_format + date_display_format
        rsa_tz = tz.gettz("Africa/Johannesburg")
        end_time_for_display = x.participant.vars["end_time"].astimezone(rsa_tz).strftime(datetime_display_format)
    elif locale == "usa":
        datetime_display_format = usa_time_format + date_display_format
        usa_tz = tz.gettz("America/New_York")
        end_time_for_display = x.participant.vars["end_time"].astimezone(usa_tz).strftime(datetime_display_format)
    else:
        end_time_for_display = x.participant.vars["end_time"]

    print("end_time_for_display: " + str(end_time_for_display))
    return end_time_for_display


class Tasks(Enum):
    risk    = 1,
    time    = 2,
    beliefs = 3,
    ca      = 4,

def get_video_url(location, task):
    url = ""
    if location == 'usa':
        if task == Tasks.risk:
            url = "https://player.vimeo.com/video/411230170"
        if task == Tasks.time:
            url = "https://player.vimeo.com/video/411230193"
        if task == Tasks.beliefs:
            url = "https://player.vimeo.com/video/411230176"
        if task == Tasks.ca:
            url = "https://player.vimeo.com/video/411230185"
    if location == 'rsa':
        if task == Tasks.risk:
            url = "https://player.vimeo.com/video/411230135"
        if task == Tasks.time:
            url = "https://player.vimeo.com/video/411230162"
        if task == Tasks.beliefs:
            url = "https://player.vimeo.com/video/411230146"
        if task == Tasks.ca:
            url = "https://player.vimeo.com/video/411230149"
    return url
