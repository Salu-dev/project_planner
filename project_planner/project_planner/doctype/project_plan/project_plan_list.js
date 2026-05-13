frappe.listview_settings["Project Plan"] = {
    add_fields: ["project", "status", "start_date", "end_date", "plan_title"],

    onload: function(listview) {
        // Add Gantt View button to toolbar
        listview.page.add_button(__("Custom Gantt View"), function() {
            frappe.set_route("project-plan-gantt");
        }, "btn-primary");
    },
	 
	gantt_custom_popup_html: function (ganttobj,plan) {
		let html = `
			<a class="text-white mb-2 inline-block cursor-pointer"
				href="/app/project-plan/${ganttobj.id}">
				${ganttobj.name}
			</a>
		`;

		if (plan.project) {
			html += `<p class="mb-1">${__("Project")}:
				<a class="text-white inline-block"
					href="/app/project/${plan.project}"">
					${plan.project}
				</a>
			</p>`;
		}
		

		if (plan._assign_to) {
			const assign_list = JSON.parse(plan._assign_to);
			const assignment_wrapper = `
				<span>Assigned to:</span>
				<span class="text-white">
					${assign_list.map((user) => frappe.user_info(user).fullname).join(", ")}
				</span>
			`;
			html += assignment_wrapper;
		}

		return `<div class="p-3" style="min-width: 220px">${html}</div>`;
	},
};
