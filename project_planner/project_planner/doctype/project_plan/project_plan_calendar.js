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
    filters: [
        {
            fieldtype: "Link",
            fieldname: "project",
            options: "Project",
            label: __("Project"),
        },
    ],
};