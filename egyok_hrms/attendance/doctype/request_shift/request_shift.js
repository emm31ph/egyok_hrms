// Copyright (c) 2024, Edmund Managuit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Request Shift", {
	refresh(frm) {

	},
    shift_type(frm){
        frappe.call({
            "method": "egyok_hrms.attendance.doctype.shift_type.shift_type.get_shift_type",
            "args": {
                "company": frm.doc.company,
                "shift_type": frm.doc.shift_type,
                "date_shift": frm.doc.date_shift,
            },
            callback(r) {
                if (r.message) {
                    var data = r.message  
                    frm.set_value('start_time', data.start_time);
                    frm.set_value('end_time', data.end_time);
                }
            }
        });
    }
});
