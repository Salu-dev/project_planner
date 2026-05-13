import frappe
from frappe import _

@frappe.whitelist()
def send_notification(doc, method):
    try:
        old_doc = doc.get_doc_before_save()
    
        if not old_doc:
            return
        # Send notification when status changes to In Review
        if old_doc.status != "In Review" and doc.status == "In Review":
            send_approval_notification(doc, "In Review")
        
        # Send notification when status changes to Approved
        if old_doc.status != "Approved" and doc.status == "Approved":
            send_approval_notification(doc, "Approved")
        
        # Send notification when status changes to Rejected
        if old_doc.status != "Rejected" and doc.status == "Rejected":
            send_approval_notification(doc, "Rejected")

        # send notification to assigned_to when status changes to Completed
        if old_doc.status != "Completed" and doc.status == "Completed":
            send_approval_notification(doc, "Completed")
    except Exception as e:
        frappe.log_error(e, "Project Plan Notification Error")
    
   
def send_approval_notification(doc, status):
    
    project_manager =  get_active_project_managers()
   
    assigned_to = doc.assigned_to
    if status == "In Review":
        if not project_manager:
            return
        subject = _("Project Plan Submitted for Review - {0}").format(doc.name)
        message = "A new project plan has been submitted for your review."
    elif status == "Approved":
        if not assigned_to:
            return
        subject = _("Project Plan Approved - {0}").format(doc.name)
        message = "Your project plan has been approved."
    elif status == "Rejected":
        if not assigned_to:
            return
        subject = _("Project Plan Rejected - {0}").format(doc.name)
        message = "Your project plan has been rejected."

    elif status == "Completed":
        if not assigned_to:
            return
        subject = _("Project Plan Tasks Completed - {0}").format(doc.name)
        message = "All tasks based on your project plan have been completed."
    else:
        # Default case for unexpected status
        return

    args = {
        "message": message,
        "project_name": doc.name,
        "start_date": doc.start_date,
        "end_date": doc.end_date,
        "assigned_to": doc.assigned_to,
        "plan_title": doc.plan_title,
        "request_url": frappe.utils.get_url_to_form("Project Plan", doc.name)
    }

    recipients = project_manager if status == "In Review" else [assigned_to] if assigned_to else []
    
    frappe.sendmail(
        template="project_plan_approval",
        recipients=recipients,
        subject=subject,
        args=args,
        header=[subject, "blue"],
        now=True,
    )
        
    
def get_active_project_managers():
    role_based_users = frappe.get_all("Has Role",
    filters={"role": "Projects Manager", "parenttype": "User", "parent": ["!=", "Administrator"]}, fields=["parent"])
    matching_users = []
    for user in role_based_users:
        # check user is enabled
        if frappe.get_value("User", user.parent, "enabled"):
            matching_users.append(user.parent)

    return matching_users


def send_review_reminder_notifications():
    """Send reminder to project managers for plans still in review with is_approved=0"""
    # Get all plans in review status with is_approved=0
    plans_in_review = frappe.get_all(
        "Project Plan",
        filters={
            "status": "In Review",
            "is_approved": 0
        },
        fields=["name", "plan_title", "start_date", "end_date", "assigned_to", "project"]
    )

    if not plans_in_review:
        return

    # Get project managers
    project_managers = get_active_project_managers()
    if not project_managers:
        return
    subject = "Project Plan Review Reminder"

    args = {
        "project_plans": plans_in_review
    }

    frappe.sendmail(
        template="project_plan_review_reminder",
        recipients=project_managers,
        subject=subject,
        args=args,
        now=True
    )


def send_task_assignment_notification(task_title, assigned_to, project_plan_name, start_date, end_date):
    """Send notification when a task is assigned to a user"""
    if not assigned_to:
        return

    # Check if user is enabled
    if not frappe.get_value("User", assigned_to, "enabled"):
        return

    subject = _("Task Assigned - {0}").format(task_title)
    message = f"You have been assigned to task: {task_title}"

    args = {
        "message": message,
        "task_title": task_title,
        "project_plan": project_plan_name,
        "start_date": start_date,
        "end_date": end_date,
        "request_url": frappe.utils.get_url_to_form("Project Plan", project_plan_name)
    }

    frappe.sendmail(
        template="task_assignment",
        recipients=[assigned_to],
        subject=subject,
        args=args,
        header=[subject, "green"],
        now=True
    )

def send_task_completion_notification(task):
    """Send notification when a task is completed"""
    if not task.custom_project_plan:
        return
    plan_assign_to = frappe.get_value("Project Plan", task.custom_project_plan, "assigned_to")

    subject = _("Task Completed - {0}").format(task.name)
    message = f"Task {task.name} has been completed"

    args = {
        "message": message,
        "task_title": task.name,
        "project_plan": task.custom_project_plan,
        "start_date": task.exp_start_date,
        "end_date": task.exp_end_date,
        "assigned_to": task.custom_assigned_to,
        "request_url": frappe.utils.get_url_to_form("Task", task.name)
    }

    frappe.sendmail(
        template="task_assignment",
        recipients=[task.custom_assigned_to],
        subject=subject,
        args=args,
        header=[subject, "green"],
        now=True
    )
