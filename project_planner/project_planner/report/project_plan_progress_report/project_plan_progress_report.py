# Copyright (c) 2026, Salu and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "project_plan",
			"label": "Project Plan",
			"fieldtype": "Link",
			"options": "Project Plan",
		},
		{
			"fieldname": "project",
			"label": "Project",
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "assigned_to",
			"label": "Assigned To",
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "total_tasks",
			"label": "Total Tasks",
			"fieldtype": "Int"
		},
		{
			"fieldname": "completed_tasks",
			"label": "Completed Tasks",
			"fieldtype": "Int"
		},
		{
			"fieldname": "completion_percentage",
			"label": "Completion %",
			"fieldtype": "Percent"
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "\nDraft\nApproved\nIn Review\nRejected\nCompleted"
		}
	]

def get_data(filters):

	data=[]
	project_plan_filter={}
	if "project" in filters:
		project_plan_filter["project"] = filters["project"]
	
	if "start_date" in filters:
		project_plan_filter["start_date"] = filters["start_date"]
	
	if "end_date" in filters:
		project_plan_filter["end_date"] = filters["end_date"]
	
	if "status" in filters:
		project_plan_filter["status"] = filters["status"]
	
	if "assigned_to" in filters:
		project_plan_filter["assigned_to"] = filters["assigned_to"]
	
	# Get project plans with the filters
	project_plans = frappe.get_all("Project Plan", filters=project_plan_filter, fields=["*"])
	
	for project_plan in project_plans:
		project_plan["project_plan"] = project_plan["name"]
		total_task=frappe.db.count("Plan Task", filters={"parent": project_plan["name"]})
		completed_task=frappe.db.count("Plan Task", filters={"parent": project_plan["name"], "status": "Completed"})
		project_plan["total_tasks"] = total_task
		project_plan["completed_tasks"] = completed_task
		project_plan["completion_percentage"] = (completed_task / total_task) * 100 if total_task > 0 else 0
		data.append(project_plan)
	
	return data
	
