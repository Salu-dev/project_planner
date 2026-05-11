# Copyright (c) 2026, Salu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ProjectPlan(Document):
	def validate(self):
		# Validate project
		self.validate_project()
		# Validate project dates
		self.validate_project_dates()
		# Validate task dates
		self.validate_task_dates()	

	def on_update(self):
		# Auto-set the Project Plan's Status to In Review when at least one Plan Task is marked as Completed.
		self.update_parent_status()

	def on_trash(self):
		# Prevent deletion of a Project Plan if its Status is Approved.
		self.prevent_deletion_if_approved()

	def validate_project(self):
		"""Validate project.	
		- Validate project is active and status is open
		- Do not consider completed and cancelled projects
		"""
		project = self.get_project()
		if (not project.is_active) or (project.status in ["Cancelled","Completed"]):
			frappe.throw("Project is not available")
		
	
	def validate_project_dates(self):
		"""Validate project plan dates.

		- Start date cannot be greater than end date
		- Project plan start date and end date should be in between project start date and end date
		"""
		if self.start_date and self.end_date:
			if self.start_date > self.end_date:
				frappe.throw("Start date cannot be greater than end date")
		if self.start_date:
			if self.start_date < self.get_project().expected_start_date:
				frappe.throw("Start date cannot be less than project start date")
		if self.end_date:
			if self.end_date > self.get_project().expected_end_date:
				frappe.throw("End date cannot be greater than project end date")

	def validate_task_dates(self):
		"""Validate task dates.
		
		- Task start date cannot be greater than task end date
		-  Validate that the Plan Task's Start Date and End Date fall within the parent 
			Project Plan's date range
		"""
		for task in self.tasks:
			if task.start_date and task.end_date:
				if task.start_date > task.end_date:
					frappe.throw("Task start date cannot be greater than task end date")
			if task.start_date:
				if task.start_date < self.start_date:
					frappe.throw("Task start date cannot be less than project start date")
			if task.end_date:
				if task.end_date > self.end_date:
					frappe.throw("Task end date cannot be greater than project end date")

	def update_parent_status(self):
		# Check if at least one task is completed
		completed_tasks = [task for task in self.tasks if task.status == "Completed"]
		if completed_tasks:
			self.status = "In Review"

	def prevent_deletion_if_approved(self):
		"""Prevent deletion of a Project Plan if its Status is Approved."""
		if self.status == "Approved" and "Administrator" not in frappe.get_roles():
			frappe.throw("Cannot delete a Project Plan with status 'Approved'")
		

	def get_project(self):
		return frappe.get_doc("Project", self.project)
