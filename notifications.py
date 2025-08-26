from canvas_connector import get_assignments_from_api, load_access_token
from config.config_manager import notif_config, load_configs, system

if system == "Windows":
    from win10toast_click import ToastNotifier
    toaster = ToastNotifier()

    def notify(assignment):
        def on_click():
            assignment.open_related_links_files()
            return 0

        toaster.show_toast(
            title=assignment.name,
            msg=assignment.notification_message(),
            icon_path=notif_config["notification_app_icon"],
            duration=notif_config["notification_duration_seconds"],
            threaded=False,
            callback_on_click=on_click
        )
        while toaster.notification_active():
            pass
elif system == "Darwin":
    from mac_notifications import client

    def notify(assignment):
        def on_click():
            assignment.open_related_links_files()
            return 0

        client.create_notification(
            title=assignment.name,
            subtitle=assignment.notification_message(),
            icon=notif_config["notification_app_icon"],
            action_button_str="Open All Links",
            action_callback=on_click
        )
else:
    from plyer import notification

    def notify(assignment):
        notification.notify(
            title=assignment.name,
            message=assignment.notification_message(),
            app_name=notif_config["notification_app_name"],
            app_icon=notif_config["notification_app_icon"],
            timeout=notif_config["notification_duration_seconds"]
        )

def dispatch(assignments):
    for assignment in assignments:
        notify(assignment)    

def dispatch_all():
    assignments = get_assignments_from_api()
    dispatch(assignments)

if __name__ == "__main__":
    load_access_token()
    load_configs()
    dispatch_all()
