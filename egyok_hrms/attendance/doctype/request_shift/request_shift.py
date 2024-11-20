# Copyright (c) 2024, Edmund Managuit and contributors
# For license information, please see license.txt

import frappe

from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import add_days, cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate

class RequestShift(Document):
	pass

	from typing import TYPE_CHECKING
	if TYPE_CHECKING:
		from frappe.types import DF
		name: DF.Link | None
		company: DF.Link | None
		employee: DF.Link | None
		amended_from: DF.Link | None
		shift_type: DF.Link | None
		employee_name: DF.Data | None
		transaction_date: DF.Date | None
		date_shift: DF.Date | None
		start_time: DF.Time | None
		end_time: DF.Time | None


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def validate(self):
		self.exist_record()

	def exist_record(self):
		res = frappe.db.exists("Request Shift", {'employee': self.employee, 'date_shift': self.date_shift,  'name': ['!=', self.name]})
		if res:
			link = frappe.utils.get_link_to_form("Request Shift", res)
			frappe.throw(_('Already applied Request Shift: {0}').format(link), title='Duplicate Request Shift')

	def on_submit(self):
		frappe.throw(f"dasdd")