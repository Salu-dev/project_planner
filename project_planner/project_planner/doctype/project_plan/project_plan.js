// Copyright (c) 2026, Salu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project Plan", {
	refresh(frm) {
        // hide project plan tab 
       frm.trigger("project_plan_tab");
    //    project filter
       frm.trigger("project_filter");

	},
    project_plan_tab(frm) {
        if (frm.is_new()) {
            frm.set_df_property("task_plan", "hidden", 1);
        }
    },
    project_filter(frm) {
       
            frm.set_query("project", function() {
                return {
                    filters: {
                        "is_active": "Yes",
                        "status": ["=", "Open"]
                    }
                };
            });
        }
});
