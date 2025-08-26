import os.path
from json import load as json_load, dump as json_dump
from platform import system as platform_system
import sys

class OutlookDistance:
    UNLIMITED = 0
    DAY = 1
    WEEK = 2
    TWO_WEEKS = 3
    END_OF_WEEK = 4

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

canvas_date_format = "%Y-%m-%dT%H:%M:%S%z"
resource_folder = "./config"
assignment_config_json = resource_folder + "/assignment_urls.json"
course_config_json = resource_folder + "/course_config.json"
general_config_json = resource_folder + "/general_config.json"
notif_config_json = resource_folder + "/notif_config.json"
system = platform_system()

course_config = {}
notif_config = {}
general_config = {}

def write_config(path, data):
    with open(path, "w") as f:
        json_dump(data, f, indent=4)
    return data

def read_config(path):
    with open(path, "r") as f:
        return json_load(f)
    
def load_config(path, defaults):
    return read_config(path) if os.path.exists(path) else write_config(path, defaults)

def load_assignments_urls(assignments):
    data = load_config(assignment_config_json, {
        str(assignment.id): [assignment.link] for assignment in assignments
    })

    for assignment in assignments:
        assignment.related_links_files = data.get(str(assignment.id), [assignment.link])

def save_assignment_related_links_files(assignment_id, related_links_files):
    data = load_config(assignment_config_json, None)
    data[str(assignment_id)] = related_links_files
    write_config(assignment_config_json, data)

def load_configs():
    global course_config, notif_config, general_config

    course_config.clear()
    course_config.update(load_config(course_config_json, dict(
        assignment_outlook_distance = OutlookDistance.WEEK,
        include_undated_assignments = False,
        include_overdue_unsubmitted_assignments = True,
        include_unsubmittable_assignments = False,
        include_submitted_assignments = False,
        using_desired_courses = False,
        desired_courses = []
    )))

    notif_config.clear()
    notif_config.update(load_config(notif_config_json, dict(
        notification_app_icon = resource_path("canvas.ico"),
        notification_app_name = "Canvas",
        notification_duration_seconds = 4,
    )))

    general_config.clear()
    general_config.update(load_config(general_config_json, dict(
        canvas_domain="http://auburn.instructure.com",
        due_date_time_format = "%m/%d/%Y at %H:%M:%S"
    )))

os.makedirs(resource_folder, exist_ok=True)
load_configs()
