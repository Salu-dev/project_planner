// Copyright (c) 2026, Salu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project Plan", {
	refresh(frm) {
    //    project filter
       frm.trigger("project_filter");
    //    assign to user filter
       frm.trigger("assign_to_user_filter");
   
	},
    project_filter(frm) {
            frm.set_query("project", function() {
                return {
                    filters: {
                        "is_active": "Yes",
                    }
                };
            });
    },
   
    assign_to_user_filter(frm) {
        if (frm.doc.project) {
            // Set query filter for assigned_to field in child table
            frm.fields_dict['task_plan'].grid.fields_map['assigned_to'].get_query = function() {
                return {
                    filters: {
                        "enabled": 1
                    }
                };
            };
        }
    }
});
