import frappe
from frappe.permissions import add_permission, update_permission_property

def after_install():
	"""Create roles, role profiles, and module profiles after installation"""
	create_project_planner_role()
	create_project_planner_role_profile()
	create_project_planner_module_profile()
	create_project_planner_permission()
	frappe.msgprint("Project Planner roles and profiles created successfully")

def create_project_planner_role():
	"""Create Project Planner role if it doesn't exist"""
	if not frappe.db.exists("Role", "Projects Manager"):
		frappe.get_doc({
			"doctype": "Role",
			"role_name": "Projects Manager",
			"desk_access": 1,
			"is_standard": 1
		}).insert()
		frappe.db.commit()

	if not frappe.db.exists("Role", "Project Member"):
		frappe.get_doc({
			"doctype": "Role",
			"role_name": "Project Member",
			"desk_access": 1,
			"is_standard": 1
		}).insert()
		frappe.db.commit()

def create_project_planner_role_profile():
	"""Create Project Planner role profile if it doesn't exist"""
	if not frappe.db.exists("Role Profile", "Projects Manager"):
		role_profile = frappe.get_doc({
			"doctype": "Role Profile",
			"role_profile": "Projects Manager",
			"is_standard": 1
		})
		role_profile.append("roles", {"role": "Projects Manager"})
		role_profile.append("roles", {"role": "Project Member"})
		role_profile.insert()
	if not frappe.db.exists("Role Profile", "Project Member"):
		role_profile = frappe.get_doc({
			"doctype": "Role Profile",
			"role_profile": "Project Member",
			"is_standard": 1
		})
		role_profile.append("roles", {"role": "Project Member"})
		role_profile.insert()
	frappe.db.commit()

def create_project_planner_module_profile():
	"""Create Project Planner module profile if it doesn't exist"""
	if not frappe.db.exists("Module Profile", "Project Planner"):
		module_profile = frappe.get_doc({
			"doctype": "Module Profile",
			"module_profile_name": "Project Planner",
			"is_standard": 1
		})
		module_profile.append("modules", {"module": "Project Planner"})
		module_profile.append("modules", {"module": "Projects"})
		module_profile.insert()
		frappe.db.commit()

def create_project_planner_permission():
	"""Create Project Planner permission"""
	#  Project plan

	doctype="Project Plan"
	role_permissions = {
        "System Manager": {
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "print": 1,
            "email": 1,
            "export": 1,
            "report": 0,
            "share": 1,
            "import": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0
        },
		"Projects Manager": {
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "print": 0,
            "email": 0,
            "export": 1,
            "report": 0,
            "share": 1,
            "import": 0,
			"submit": 1,
			"cancel": 0,
			"amend": 1
        },
		"Project Member": {
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0,
            "print": 0,
            "email": 0,
            "export": 1,
            "report": 0,
            "share": 0,
            "import": 0,
			"submit": 0,
			"cancel": 0,
			"amend": 0
        },
    }
	for role, permissions in role_permissions.items():
		add_permission(doctype, role, **permissions)
		frappe.db.commit()

	# Add Project doctype read permissions for both roles
	add_permission("Project", "Projects Manager", read=1, report=1)
	add_permission("Project", "Project Member", read=1, report=1)
	frappe.db.commit()

