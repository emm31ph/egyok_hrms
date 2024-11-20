egyok_core.TransactionController = class TransactionController extends egyok_hrms.shit_type {
    shit_type() {
        console.log("shift type");

        // frappe.call({
        //     method: "egyok_hrms.controllers.utils.get_shift_type",
        //     args: {
        //         terms_template: doc.payment_terms_template,
        //         posting_date: posting_date,
        //         grand_total: doc.rounded_total || doc.grand_total,
        //         base_grand_total: doc.base_rounded_total || doc.base_grand_total,
        //         bill_date: doc.bill_date
        //     },
        //     callback: function(r) {
        //         if (r.message && !r.exc) {
        //             me.frm.set_value("payment_schedule", r.message);
        //             const company_currency = me.get_company_currency();
        //             me.update_payment_schedule_grid_labels(company_currency);
        //         }
        //     }
        // })
    }
}