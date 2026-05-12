import frappe

def project_plan_permission(user):
    if not user:
        user=frappe.session.user
        
    if "Project Manager" in frappe.get_roles(user) or "Administrator" in frappe.get_roles(user):
        return ""

    if "Project Member" in frappe.get_roles(user):
        
        return f"""
            (
                `tabProject Plan`.owner = '{user}'
                OR
                `tabProject Plan`.assigned_to = '{user}'
                OR
                (
                    `tabProject Plan`.name IN (
                        SELECT parent
                        FROM `tabPlan Task`
                        WHERE assigned_to = '{user}'
                    )
                    AND `tabProject Plan`.status = 'Approved'
                )
            )
        """