frappe.views.calendar["Project Plan"] = {
    field_map: {
        start: "start_date",
        end: "end_date",
        id: "name",
        allDay: "all_day",
        title: "plan_title",
        status: "status",
    },
    gantt: true,
    get_events_method: "project_planner.project_planner.api.get_gantt_events",
    filters: [
        {
            fieldtype: "Link",
            fieldname: "project",
            options: "Project",
            label: __("Project"),
        },
    ],
};