import frappe
from frappe import _
from project_planner.project_planner.notification import send_task_completion_notification


def task_on_update(doc, method):

    if not doc.custom_project_plan:
        return
    old_doc = doc.get_doc_before_save()
    if old_doc and old_doc.status!=doc.status:
        if doc.status in ["Open","Working", "Completed"]:
            sync_task_status_to_child_table(doc, old_doc)
            update_parent_status(doc.custom_project_plan)

def sync_task_status_to_child_table(doc, old_doc):

    """Update Project Plan child table task status based on Task status update"""

    if doc.status == "Working":
        status="In Progress"
    elif doc.status == "Completed":
        status="Completed"
        send_task_completion_notification(doc)
    else:
        return

    # get child table row
    if doc.custom_project_plan:
        project_plan_task = frappe.get_value("Plan Task", {"task_id": doc.name}, "name")
        if project_plan_task:
            frappe.db.set_value("Plan Task", project_plan_task, "status", status)
    frappe.db.commit()


def update_parent_status(project_plan):
    """Update Project Plan status based on child task statuses"""
    doc = frappe.get_doc("Project Plan", project_plan)
    statuses = [task.status for task in doc.task_plan]
    # if all completed
    if statuses and all(s == "Completed" for s in statuses):
        new_status = "Completed"
    # if any completed
    elif "Completed" in statuses:
        new_status = "In Review"
    else:
        new_status = "Approved"

    frappe.db.set_value("Project Plan", project_plan, "status", new_status)
    frappe.db.set_value("Project Plan", project_plan, "workflow_state", new_status)
    frappe.db.commit()