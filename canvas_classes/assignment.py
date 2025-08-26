from config.config_manager import canvas_date_format, general_config, save_assignment_related_links_files, system
from datetime import datetime
from os import startfile as os_startfile
from os.path import exists as os_path_exists
import subprocess
import webbrowser

class Assignment:
    def __init__(self, data, course):
        self.course = course
        self.id = data["id"]
        self.name = data["name"]
        self.accepts_submissions = not ("none" in data["submission_types"])
        self.due_date = datetime.strptime(data["due_at"], canvas_date_format).astimezone() if data["due_at"] is not None else None
        self.has_submission = data["has_submitted_submissions"]
        self.is_overdue = self.due_date is not None and self.due_date < datetime.now().astimezone()
        self.link = general_config["canvas_domain"] + "/courses/" + str(course.id) + "/assignments/" + str(self.id)
        self.related_links_files = []
        
    def notification_message(self):
        if self.due_date is None:
            return "No Due Date"
        return "Due Date: " + datetime.strftime(self.due_date, general_config["due_date_time_format"])

    def open_related_links_files(self):
        print(self.related_links_files)
        for related_link_file in self.related_links_files:
            if related_link_file.startswith(("http://", "https://")):
                webbrowser.open(related_link_file, new=2)
            elif os_path_exists(related_link_file):
                if system == "Windows":
                    os_startfile(related_link_file)
                elif system == "Darwin":
                    subprocess.call(["open", related_link_file])
                else:
                    subprocess.call(["xdg-open", related_link_file])
    
    def save_related_links_files(self, related_links_files):
        self.related_links_files = related_links_files
        save_assignment_related_links_files(self.id, self.related_links_files)

    def to_json(self):
        return {
            "course_name": self.course.name,
            "id": self.id,
            "name": self.name,
            "due_date": datetime.strftime(self.due_date, general_config["due_date_time_format"]) if self.due_date is not None else "No Due Date",
            "is_overdue": self.is_overdue,
            "link": self.link,
            "related_links_files": self.related_links_files
        }
    