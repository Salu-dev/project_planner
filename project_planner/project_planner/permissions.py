import frappe

def project_plan_permission(user):
    if not user:
        user=frappe.session.user
    # Projects Manager and Administrator have full access
    if "Projects Manager" in frappe.get_roles(user) or "Administrator" in frappe.get_roles(user):
        
        return ""

    # Project Member: can view/update own created, assigned to, or task assignee in approved plans
    if "Project Member" in frappe.get_roles(user):
        condition = f"""
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
        
        return condition

    # If user has none of the roles, deny access
    frappe.log_error(f"Access denied for {user}", "Project Plan Permission Debug")
    return "1=0"