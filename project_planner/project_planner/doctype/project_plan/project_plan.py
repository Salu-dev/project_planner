# Copyright (c) 2026, Salu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from project_planner.project_planner.notification import send_task_assignment_notification


class ProjectPlan(Document):
	def validate(self):
		# Validate project
		self.validate_project()
		# Validate project dates
		self.validate_project_dates()
		# Validate task dates
		self.validate_task_dates()	
		# Ensure atleast one task plan before submit for review
		self.validate_task_plan_count()
		# Validate task status
		self.validate_task_status()

	def on_update(self):
		# Auto-set the Project Plan's Status to In Review when at least one Plan Task is marked as Completed.
		self.update_parent_status()
		
	def on_submit(self):
		if self.status == "Approved":
			self.update_parent_fields()
			self.update_project_users()
			self.auto_create_tasks()

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
		project_start = frappe.utils.getdate(self.start_date)
		project_end = frappe.utils.getdate(self.end_date)
		for task in self.task_plan:
			task_start = frappe.utils.getdate(task.start_date)
			task_end = frappe.utils.getdate(task.end_date)
			if task_start and task_end:
				if task_start > task_end:
					frappe.throw("Task start date cannot be greater than task end date")
				if task_start < project_start:
					frappe.throw("Task start date cannot be less than project start date")
				if task_end > project_end:
					frappe.throw("Task end date cannot be greater than project end date")

	def validate_task_plan_count(self):
		"""
		- Atleast one task plan should be there before submit for review
		"""
		if self.status != "Draft" and not self.task_plan:
			frappe.throw("Atleast one task plan should be there before submit for review")

	def validate_task_status(self):
		"""Validate task status.
		
		- Task status cannot be Approved if project plan is not approved
		"""
		if self.status != "Approved":
			for task in self.task_plan:
				if task.status == "Approved":
					frappe.throw("Task status cannot be Approved if project plan is not approved")

	def update_parent_status(self):
		# Check if at least one task is completed
		completed_tasks = [task for task in self.task_plan if task.status == "Completed"]
		if completed_tasks:
			self.db_set("status", "In Review")

	def update_parent_fields(self):
		"""Update parent fields when project plan is submitted."""
		self.db_set("approved_by", frappe.session.user)
		self.db_set("approved_on", frappe.utils.now_datetime())
		self.db_set("is_approved", 1)

	def update_project_users(self):
		"""Update project users when project plan is Approved."""
		project = frappe.get_doc("Project", self.project)
		# Check if user already exists in custom_team_members to avoid duplication
		existing_users = [member.user for member in project.custom_team_members]
		if self.assigned_to not in existing_users:
			project.append("custom_team_members", {
				"user": self.assigned_to
			})
		for task in self.task_plan:
			if task.assigned_to not in existing_users:
				project.append("custom_team_members", {
					"user": task.assigned_to
				})		
		project.save()
	
	def auto_create_tasks(self):
		"""Auto-create tasks for the project plan."""
		
		try:
			for plan_task in self.task_plan:
				if not plan_task.task_id:
					new_task = frappe.new_doc("Task")
					new_task.subject = plan_task.task_title
					new_task.project = self.project
					new_task.priority = plan_task.priority
					new_task.exp_start_date = plan_task.start_date
					new_task.exp_end_date = plan_task.end_date
					new_task.custom_assigned_to = plan_task.assigned_to
					new_task.custom_project_plan = self.name
					new_task.insert(ignore_permissions=True)
					frappe.db.set_value("Plan Task", plan_task.name, "task_id", new_task.name)
					# Send notification to assigned user
					if plan_task.assigned_to:
						send_task_assignment_notification(
							task_title=plan_task.task_title,
							assigned_to=plan_task.assigned_to,
							project_plan_name=self.name,
							start_date=plan_task.start_date,
							end_date=plan_task.end_date
						)
		except Exception as e:
			frappe.log_error(e, "Project Plan Auto Create Tasks Error")	

	def prevent_deletion_if_approved(self):
		"""Prevent deletion of a Project Plan if its Status is Approved."""
		if self.is_approved and "Administrator" not in frappe.get_roles():
			frappe.throw("Cannot delete a Project Plan with status 'Approved'")
		

	def get_project(self):
		return frappe.get_doc("Project", self.project)


@frappe.whitelist()
def get_project_users(doctype, txt, searchfield, start, page_len, filters):
	"""Get users assigned to a project"""
	project = filters.get("project") if filters else None
	if not project:
		return []
	user_filters = {"parent": project}
	if txt:
		user_filters["user"] = ["like", f"%{txt}%"]
	
	users = frappe.get_all(
		"Project User",
		filters=user_filters,
		fields=["user","full_name"]
	)
	return [[user.user,user.full_name, ] for user in users]
