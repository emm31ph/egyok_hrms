frappe.ui.form.on("Shift Type", {
    onload(frm) {
        if (frm.is_new()) {
            initialize_shift_details(frm);
        }
        disable_add_delete_in_child_table(frm);
    },
    start_time: function(frm) {
        update_child_times_and_working_hours(frm);
    },
    end_time: function(frm) {
        update_child_times_and_working_hours(frm);
    }
});

function initialize_shift_details(frm) {
    const days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    frm.clear_table("shift_type_details");

    days_of_week.forEach(day => {
        let row = frm.add_child("shift_type_details");
        row.work_days = day;
        row.break = 1;
    });

    frm.refresh_field("shift_type_details");
}

function disable_add_delete_in_child_table(frm) {
    frm.set_df_property('shift_type_details', 'cannot_add_rows', true);
    frm.set_df_property('shift_type_details', 'cannot_delete_rows', true);
    frm.set_df_property('shift_type_details', 'cannot_delete_all_rows', true);
}

function update_child_times_and_working_hours(frm) {
    if (!frm.doc.start_time || !frm.doc.end_time) return;

    const parent_start = moment(frm.doc.start_time, "HH:mm:ss");
    const parent_end = moment(frm.doc.end_time, "HH:mm:ss");

    frm.doc.shift_type_details.forEach(row => {
        row.start_time = parent_start.format("HH:mm:ss");
        row.end_time = parent_end.format("HH:mm:ss");

        let working_hours = moment.duration(parent_end.diff(parent_start)).asHours();
        row.working_hours = Math.max(working_hours - (row.break ? 1 : 0), 0);
    });

    frm.refresh_field("shift_type_details");
}

frappe.ui.form.on('Shift Type Details', {
    start_time: function(frm, cdt, cdn) {
        calculate_row_working_hours(frm, cdt, cdn);
    },
    end_time: function(frm, cdt, cdn) {
        calculate_row_working_hours(frm, cdt, cdn);
    },
    break: function(frm, cdt, cdn) {
        calculate_row_working_hours(frm, cdt, cdn);
    }
});

function calculate_row_working_hours(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (!row.start_time || !row.end_time) return;

    const row_start = moment(row.start_time, "HH:mm:ss");
    const row_end = moment(row.end_time, "HH:mm:ss");
    let working_hours = moment.duration(row_end.diff(row_start)).asHours();

    row.working_hours = Math.max(working_hours - (row.break ? 1 : 0), 0);
    frm.refresh_field("shift_type_details");
}
