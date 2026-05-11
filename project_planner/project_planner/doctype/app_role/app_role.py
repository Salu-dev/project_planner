# Copyright (c) 2026, Salu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AppRole(Document):
	def after_insert(self):
		"""Create Frappe Role if it doesn't exist."""
		if not frappe.db.exists("Role", self.role):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": self.role
			}).insert()
	
