// Copyright (c) 2024, Edmund Managuit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Import Logs", {
    after_save(frm){
        frm.reload_doc(); // Reload the document to fetch changes
    },
	refresh(frm) {
        if (frm.doc.docstatus === 0 && !frm.doc.__islocal) {
            frm.add_custom_button(__("Fetch Logs"), function() {
                let d = new frappe.ui.Dialog({
                    title: __("Import Logs"),
                    fields: [{
                            label: __("From"),
                            fieldname: "from_date",
                            fieldtype: "Date",
                            default: "Today",
                            reqd: 1,
                        },
                        {
                            label: __("To"),
                            fieldname: "to_date",
                            fieldtype: "Date",
                            default: "Today",
                            reqd: 1,
                        },
                        {
                            label: 'CSV File',
                            fieldname: 'csv_file',
                            fieldtype: 'Attach',
                            reqd: 1
                        }
                    ],
                    primary_action: function(values) {
                        frm.set_value('att_from_date', values.from_date)
                        frm.set_value('att_to_date', values.to_date)
                        frappe.call({
                            method: 'egyok_hrms.attendance.doctype.import_logs.import_logs.upload_csv',
                            args: {
                                docname: frm.doc.name,
                                doctype: frm.doc.doctype,
                                from_date: values.from_date,
                                to_date: values.to_date,
                                csv_file: values.csv_file
                            },
                            callback: function(r) {
                                console.log(r.message);
                                
                                frm.set_value('import_log_details', [])
                                if (r.message.status === 'success') {
                                    const attendance_data = r.message.dat_list;
                                    console.log(r.message);

                                    attendance_data.forEach(entry => {
                                        let child = frm.add_child('import_log_details');
                                        child.biometric_id = entry.biometric_id;
                                        child.employee = entry.employee;
                                        child.employee_name = entry.employee_name;
                                        child.date = entry.date;
                                        child.time = entry.time;
                                        child.log_type = entry.log_type_text;
                                        child.trn_datetime = entry.trn_datetime;
                                        // child.remarks = entry.remarks;

                                    });
                                    frm.refresh_field('import_log_details');
                                    frappe.msgprint(__('Attendance data has been appended successfully.'));

                                } else {
                                    frappe.msgprint({
                                        title: __('Error'),
                                        indicator: 'red',
                                        message: r.message.message
                                    });
                                }
                            }
                        });
                        // d.hide();

                    },
                    primary_action_label: __("Get Logs"),
                });
                d.show();
            });
        }
	},
});
