# Copyright (c) 2024, Edmund Managuit and contributors
# For license information, please see license.txt

import frappe
from frappe import _, scrub
from datetime import datetime

from frappe.model.document import Document


class ShiftType(Document):
	pass




@frappe.whitelist()
def get_shift_type(company,shift_type,date_shift):
	shift_type = frappe.get_doc("Shift Type",  shift_type)
	date_obj = datetime.strptime(date_shift, '%Y-%m-%d')  # Example format: '2024-11-15'
	dayname = date_obj.strftime('%A')  # '%A' gives the full weekday name
	schedule = []
	for d in shift_type.get("shift_type_details"):
		if dayname == d.work_days:
		# term_details = get_payment_term_details(d, posting_date, grand_total, base_grand_total, bill_date)
			return frappe._dict({"start_time":d.start_time,"end_time":d.end_time,"work_days":d.work_days})

	return schedule
