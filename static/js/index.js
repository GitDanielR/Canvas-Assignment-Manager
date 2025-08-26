document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.assignment-row').forEach(function(row) {
        row.addEventListener('click', function(e) {
            const assignmentId = row.getAttribute('data-id');
            if (e.target.classList.contains('assignment-open-all')) {
                fetch(`/assignments/${assignmentId}/open_related_links_files`, { method: 'POST' });
            } else {
                window.location.href = `/assignments/${assignmentId}`;
            }
        });
    });

    const settingsBtn = document.getElementById('settings-btn');
    const modal = document.getElementById('settings-modal');
    const closeModal = document.getElementById('close-settings-modal');
    const form = document.getElementById('settings-form');

    function fillSettingsForm() {
        form.assignment_outlook_distance.value = courseConfig.assignment_outlook_distance;
        form.include_undated_assignments.checked = courseConfig.include_undated_assignments;
        form.include_overdue_unsubmitted_assignments.checked = courseConfig.include_overdue_unsubmitted_assignments;
        form.include_unsubmittable_assignments.checked = courseConfig.include_unsubmittable_assignments;
        form.include_submitted_assignments.checked = courseConfig.include_submitted_assignments;
        form.using_desired_courses.checked = courseConfig.using_desired_courses;
        form.desired_courses.value = (courseConfig.desired_courses || []).join(', ');

        form.notification_app_icon.value = notifConfig.notification_app_icon;
        form.notification_app_name.value = notifConfig.notification_app_name;
        form.notification_duration_seconds.value = notifConfig.notification_duration_seconds;
        
        form.canvas_domain.value = generalConfig.canvas_domain;
        form.due_date_time_format.value = generalConfig.due_date_time_format;
    }

    settingsBtn.addEventListener('click', () => {
        fillSettingsForm();
        modal.style.display = 'flex';
    });
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const destroyToast = showToast('Saving settings & reloading assignments...');
        const data = {
            course_config: {
                assignment_outlook_distance: parseInt(form.assignment_outlook_distance.value),
                include_undated_assignments: form.include_undated_assignments.checked,
                include_overdue_unsubmitted_assignments: form.include_overdue_unsubmitted_assignments.checked,
                include_unsubmittable_assignments: form.include_unsubmittable_assignments.checked,
                include_submitted_assignments: form.include_submitted_assignments.checked,
                using_desired_courses: form.using_desired_courses.checked,
                desired_courses: form.desired_courses.value.split(',').map(s => s.trim()).filter(Boolean)
            },
            notif_config: {
                notification_app_icon: form.notification_app_icon.value,
                notification_app_name: form.notification_app_name.value,
                notification_duration_seconds: parseInt(form.notification_duration_seconds.value),
            },
            general_config: {
                canvas_domain: form.canvas_domain.value,
                due_date_time_format: form.due_date_time_format.value
            }
        };
        fetch('/update_configs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(res => {
            if (res.ok) {
                destroyToast();
                modal.style.display = 'none';
                showToast('Settings saved!');
                setTimeout(() => location.reload(), 1000);
            } else {
                showToast('Failed to save settings.');
            }
        });
    });
});
