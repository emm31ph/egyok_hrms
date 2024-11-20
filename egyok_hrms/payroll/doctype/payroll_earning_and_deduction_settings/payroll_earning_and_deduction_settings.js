// Copyright (c) 2024, Edmund Managuit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Payroll Earning and Deduction Settings", {
    refresh(frm) {
        // frm.set_value('sss_rates', [])
        // let reg_er = 380;
        // let reg_ee = 180;
        // let wisp_ee = 22.50;
        // let wisp_er = 47.50;
        // for (let index = 4250; index <= 29750; index += 500) {
        //     let from_amount = index;
        //     let to_amount = index - 0.01;
        //     reg_er += 47.5
        //     reg_ee += 22.5
        //     if (from_amount >= 19750) {
        //         reg_er = 1900
        //     }
        //     if (from_amount >= 20250) {
        //         reg_ee = 900
        //     }
        //     let row = frm.add_child("sss_rates");
        //     row.from_amount = from_amount;
        //     row.to_amount = to_amount;
        //     row.ee = reg_ee;
        //     row.er = reg_er;
        //     if (from_amount >= 20250) {
        //         row.wisp_ee = wisp_ee;
        //         row.wisp_er = wisp_er;
        //         wisp_er += 47.5;
        //         wisp_ee += 22.5;

        //     }
        // }
        // frm.refresh_field("sss_rates");
    },
});