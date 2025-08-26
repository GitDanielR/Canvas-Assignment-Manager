from config.config_manager import course_config, general_config, OutlookDistance, load_assignments_urls
from canvas_classes import assignment, course
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from os import getenv
import requests

ACCESS_TOKEN = None
HEADERS = None
PARAMS = dict(
    enrollment_state = "active"
)

def load_access_token():
    global ACCESS_TOKEN, HEADERS

    load_dotenv()
    ACCESS_TOKEN = getenv("CANVAS_ACCESS_TOKEN")
    assert ACCESS_TOKEN is not None and ACCESS_TOKEN != "", "Invalid canvas access token. Should have a .env file with CANVAS_ACCESS_TOKEN={YOUR_TOKEN}."
    HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}

def is_course_desired(course):
    if len(course_config["desired_courses"]) == 0:
        return False
    return any(desired_course in course.name for desired_course in course_config["desired_courses"])

def assignment_within_outlook(assignment):
    if assignment.due_date is None:
        return course_config["include_undated_assignments"]

    outlook_distance = course_config["assignment_outlook_distance"]
    due_date = assignment.due_date.date()
    today = datetime.now().astimezone().date()
    if outlook_distance == OutlookDistance.DAY:
        return due_date == today
    if outlook_distance == OutlookDistance.WEEK:
        return timedelta(days=0) <= (due_date - today) <= timedelta(days=7)
    if outlook_distance == OutlookDistance.TWO_WEEKS:
        return timedelta(days=0) <= (due_date - today) <= timedelta(days=14)
    if outlook_distance == OutlookDistance.END_OF_WEEK:
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        return today <= due_date <= end_of_week
    return True # OutlookDistance.UNLIMITED

def assignment_matches_submittal_filters(assignment):
    matches_filter = True
    if not course_config["include_unsubmittable_assignments"]:
        matches_filter &= assignment.accepts_submissions
    if not course_config["include_submitted_assignments"]:
        matches_filter &= not assignment.has_submission
    if course_config["include_overdue_unsubmitted_assignments"]:
        matches_filter |= (assignment.is_overdue and assignment.accepts_submissions and not assignment.has_submission)
    return matches_filter

def get_courses():
    all_courses = [
        course.Course(data) for data in
        requests.get(f"{general_config['canvas_domain']}/api/v1/courses", headers=HEADERS, params=PARAMS).json()
    ]
    if course_config["using_desired_courses"] == True:
        filtered_courses = [course for course in all_courses if is_course_desired(course)]
    else:
        filtered_courses = all_courses
    return filtered_courses, all_courses

def get_courses_and_assignments_from_api():
    filtered_courses, all_courses = get_courses()
    assignments = get_assignments_from_api(filtered_courses)
    return all_courses, assignments

def get_assignments_from_api(_courses=None):
    courses = _courses if _courses is not None else get_courses()[0]
    
    filtered_assignments = []
    for course in courses:
        course_assignments = [
            assignment.Assignment(data, course) for data in
            requests.get(f"{general_config['canvas_domain']}/api/v1/courses/{course.id}/assignments", headers=HEADERS).json()
        ]
        filtered_assignments.extend([
            course_assignment for course_assignment in
            course_assignments if
            assignment_within_outlook(course_assignment) and assignment_matches_submittal_filters(course_assignment) 
        ])
    load_assignments_urls(filtered_assignments)
    return filtered_assignments

def get_assignment(assignments, assignment_id):
    for assignment in assignments:
        if assignment.id == assignment_id:
            return assignment
    return None
