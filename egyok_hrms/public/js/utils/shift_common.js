frappe.provide("egyok_hrms.attendance");

egyok_hrms.shift_common = {
    setup_shift_controller: function() {
        egyok_hrms.attendance.ShiftController = class ShiftController extends egyok_hrms.TransactionController {

            // console.log("shift common");
        }
    }
}