from flask import Flask, jsonify, render_template, request
from canvas_connector import get_assignment, get_courses_and_assignments_from_api, load_access_token
from config import config_manager
from os import _exit as os_exit
import signal
import webbrowser

app = Flask("Canvas Assignment Manager", template_folder=config_manager.resource_path("templates"), static_folder=config_manager.resource_path("static"))
assignments = []
courses = []

@app.route("/")
def index():
    assignments_data = [assignment.to_json() for assignment in assignments]
    courses_data = [course.to_json() for course in courses]
    return render_template("index.html", 
                           assignments=assignments_data,
                           courses=courses_data, 
                           OutlookDistance=config_manager.OutlookDistance,
                           course_config=config_manager.course_config,
                           notif_config=config_manager.notif_config,
                           general_config=config_manager.general_config)

@app.route("/assignments/<int:assignment_id>", methods=["GET"])
def get_assignment_page(assignment_id):
    assignment = get_assignment(assignments, assignment_id)
    if assignment is None:
        return jsonify({"status": "failure"}), 404
    return render_template("assignment.html", assignment=assignment.to_json())

@app.route("/assignments/<int:assignment_id>/open_related_links_files", methods=["POST"])
def open_related_links_files(assignment_id):
    assignment = get_assignment(assignments, assignment_id)
    if assignment is not None:
        assignment.open_related_links_files()
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"})

@app.route("/assignments/<int:assignment_id>/save_related_links_files", methods=["POST"])
def save_related_links_files(assignment_id):
    assignment = get_assignment(assignments, assignment_id)
    if assignment is not None:
        related_links_files = request.json.get("related_links_files", [])
        assignment.save_related_links_files(related_links_files)
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"})

@app.route("/update_configs", methods=["POST"])
def update_configs():
    data = request.get_json()

    try:
        config_manager.write_config(config_manager.course_config_json, data["course_config"])
        config_manager.write_config(config_manager.notif_config_json, data["notif_config"])
        config_manager.write_config(config_manager.general_config_json, data["general_config"])
        
        reload_resources()
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "failure", "error": str(e)}), 500

@app.route("/shutdown", methods=["POST"])
def shutdown():
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()
    os_exit(0)

def signal_handler(sig, frame):
    os_exit(0)

def reload_resources():
    global courses, assignments
    config_manager.load_configs()
    courses, assignments = get_courses_and_assignments_from_api()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    load_access_token()
    courses, assignments = get_courses_and_assignments_from_api()

    webbrowser.open("http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
