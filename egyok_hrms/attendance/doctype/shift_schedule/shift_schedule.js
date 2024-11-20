// Copyright (c) 2024, Edmund Managuit and contributors
// For license information, please see license.txt

egyok_hrms.shift_common.setup_shift_controller();

frappe.ui.form.on("Shift Schedule", {
    setup: function(frm) {
        frm.set_query("employee", function(doc) {
            return {
                filters: {
                    company: frm.doc.company,
                },
            };
        });
        frm.set_query("shift_type", function(doc) {
            return {
                filters: {
                    company: frm.doc.company,
                },
            };
        });
    },
    refresh(frm) {

    },
});