frappe.listview_settings["Project Plan"] = {
	add_fields: [
		"project",
		"status",
		"start_date",
		"end_date",
		"plan_title",
	],
	filters: [["status", "=", "Draft"]],
	onload: function (listview) {
		var method = "erpnext.projects.doctype.task.task.set_multiple_status";

		listview.page.add_menu_item(__("Set as Open"), function () {
			listview.call_for_selected_items(method, { status: "Open" });
		});

		listview.page.add_menu_item(__("Set as Completed"), function () {
			listview.call_for_selected_items(method, { status: "Completed" });
		});
	},
	get_indicator: function (doc) {
		var colors = {
			Draft: "gray",
			"In Review": "orange",
			Approved: "green",
		};
		return [__(doc.status), colors[doc.status], "status,=," + doc.status];
	},
	gantt_custom_popup_html: function (ganttobj,plan) {
		let html = `
			<a class="text-white mb-2 inline-block cursor-pointer"
				href="/app/task/${ganttobj.id}"">
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
