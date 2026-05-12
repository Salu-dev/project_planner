// Copyright (c) 2026, Salu and contributors
// For license information, please see license.txt

frappe.query_reports["Project Plan Progress Report"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": "Project",
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -30)
		},
		
		{
			"fieldname": "end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "assigned_to",
			"label": "Assigned To",
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "\nDraft\nApproved\nIn Review\nRejected",
			"default": "Approved"
		}

	]
};
