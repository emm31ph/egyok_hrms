(() => {
  // ../egyok_hrms/egyok_hrms/public/js/utils/shift_common.js
  frappe.provide("egyok_hrms.attendance");
  egyok_hrms.shift_common = {
    setup_shift_controller: function() {
      egyok_hrms.attendance.ShiftController = class ShiftController extends egyok_hrms.TransactionController {
      };
    }
  };
})();
//# sourceMappingURL=egyok_hrms.bundle.EAVTX5MT.js.map
