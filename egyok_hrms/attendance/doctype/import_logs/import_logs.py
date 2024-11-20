# Copyright (c) 2024, Edmund Managuit and contributors
# For license information, please see license.txt

import frappe
import os
import json
from frappe.utils import get_url
from frappe import _
from frappe.model.document import Document
from datetime import datetime, timedelta
from collections import defaultdict
from operator import itemgetter

class ImportLogs(Document):

	def on_submit(self):
		child_table_data = self.import_log_details
		child_table_array = []

		# Populate child table data
		for row in child_table_data:
			trn_datetime = f"{row.date} {row.time}"
			child_table_array.append({
				"employee": row.employee,
				"date": row.date,
				"time": row.time,
				"log_type": row.log_type,
				"trn_datetime": trn_datetime,
			})

		# Sort and group data by employee
		# sorted_data = sorted(child_table_array, key=itemgetter("employee", "trn_datetime"))
		sorted_data = sorted(
			child_table_array,
			key=lambda x: (x['employee'], x['date'], time_to_seconds(x['time']))
		)
		grouped_data = defaultdict(list)
		for log in sorted_data:
			grouped_data[log["employee"]].append(log)

		products = []
		for employee, logs in grouped_data.items():
			trn_date_count = defaultdict(int)
			for log in logs:
				trn_date_count[log["date"]] += 1

			last_in_item = {  # Initialize with empty values
				"employee": "", "trn_date": "", "date_in": "", "time_in": "", "date_out": "", "time_out": "",
				"trn_datetime_in": "", "trn_datetime_out": "", "remarks": "",
			}

			# Process logs
			for log in logs:
				if log["log_type"] == "In":
					self._process_in_log(log, last_in_item, products, trn_date_count)
				elif log["log_type"] == "Out":
					self._process_out_log(log, last_in_item, products, trn_date_count)

			# Handle remaining unmatched "In"
			self._handle_remaining_in(last_in_item, products, trn_date_count)

		# Validate remarks before submission
		self._validate_remarks(products)

	def _process_in_log(self, log, last_in_item, products, trn_date_count):
		if last_in_item["date_in"] and not last_in_item["date_out"]:
			products.append({
				"employee": last_in_item["employee"],
				"trn_date": last_in_item["date_in"],
				"date_in": last_in_item["date_in"],
				"time_in": last_in_item["time_in"],
				"date_out": "", "time_out": "",
				"trn_datetime_in": last_in_item["trn_datetime_in"],
				"trn_datetime_out": "", "count": 1, "remarks": "No Out",
			})
			last_in_item.update({key: "" for key in last_in_item})

		last_in_item.update({
			"employee": log["employee"], "trn_date": log["date"], "date_in": log["date"], "time_in": log["time"],
			"trn_datetime_in": log["trn_datetime"], "trn_datetime_out": "", "remarks": "",
		})

	def _process_out_log(self, log, last_in_item, products, trn_date_count):
		if last_in_item["date_in"]:
			last_in_item.update({
				"date_out": log["date"], "time_out": log["time"], "trn_datetime_out": log["trn_datetime"],
				"remarks": "",
			})
			products.append(self._get_product_data(last_in_item, trn_date_count))
			last_in_item.update({key: "" for key in last_in_item})
		else:
			products.append({
				"employee": log["employee"], "trn_date": log["date"], "trn_datetime_in": "",
				"trn_datetime_out": log["trn_datetime"], "date_in": "", "time_in": "",
				"date_out": log["date"], "time_out": log["time"], "count": 1, "remarks": "No In",
			})

	def _handle_remaining_in(self, last_in_item, products, trn_date_count):
		if last_in_item["date_in"] and not last_in_item["date_out"]:
			products.append(self._get_product_data(last_in_item, trn_date_count))

	def _get_product_data(self, last_in_item, trn_date_count):
		return {
			"employee": last_in_item["employee"], "trn_date": last_in_item["trn_date"],
			"date_in": last_in_item["date_in"], "time_in": last_in_item["time_in"], "date_out": last_in_item["date_out"],
			"time_out": last_in_item["time_out"], "trn_datetime_in": last_in_item["trn_datetime_in"],
			"trn_datetime_out": last_in_item["trn_datetime_out"], "count": trn_date_count[last_in_item["trn_date"]],
			"remarks": last_in_item["remarks"],
		}

	def _validate_remarks(self, products):
		json_display = json.dumps(products, indent=4)
		print(json_display)
		for product in products:
			if product["remarks"]:
				employee= product['employee']
				url = self.get('name')	
				doctype = self.get('doctype')	
				print_url = f"{get_url()}/app/print/{doctype}/{url}?filters[employee]={employee}"
				frappe.throw(_("Submission not allowed: Employee {0} has an issue on {1} ({2}). <a href='{3}' target='_blank'>click here!</a>").format(
                    product['employee'], product['trn_date'], product['remarks'],print_url
                ))

	def before_save(self):
		
		# Ensure `att_from_date` and `att_to_date` are defined
		if not (self.att_from_date and self.att_to_date):
			frappe.throw(_("Attendance from date and to date must be defined"))

		# Convert date strings to date objects for comparison
		att_from_date = datetime.strptime(self.att_from_date, "%Y-%m-%d").date()
		att_to_date = datetime.strptime(self.att_to_date, "%Y-%m-%d").date()

		# Filter the records to include only those within the date range
		filtered_details = []
		for detail in self.import_log_details:
			# Convert detail.date to a date object if it's not already
			try:
				detail_date = datetime.strptime(detail.date, "%Y-%m-%d").date()
			except ValueError:
				continue  # Skip invalid date formats

			if att_from_date <= detail_date <= att_to_date:
				filtered_details.append(detail)

		# Sort the filtered records
		sorted_details = sorted(
			filtered_details,
			key=lambda x: (x.employee, x.date, time_to_seconds(x.time))
		)

		# Update idx and assign back to `import_log_details`
		for idx, detail in enumerate(sorted_details, start=1):
			print(f"{idx} {detail.time}")
			detail.idx = idx

		self.import_log_details = sorted_details

def time_to_seconds(time_str):
		"""Convert time string (HH:MM:SS) to total seconds."""
		try:
			t = datetime.strptime(time_str, "%H:%M:%S").time()
			return t.hour * 3600 + t.minute * 60 + t.second
		except ValueError:
			return 0  # Handle invalid time strings gracefully

@frappe.whitelist(allow_guest=True)
def upload_csv(docname, doctype, from_date, to_date, csv_file):
	if os.path.splitext(csv_file)[1] != '.dat':
		frappe.throw(_("Only .dat files are supported for upload."))
		
	return dat_function(docname, doctype, from_date, to_date, csv_file)


@frappe.whitelist()
def get_logs(docname, doctype):
	doc = frappe.get_doc('Import Logs', docname)
	item_details = [
		{
			"biometric_id": int(item.biometric_id),
			"employee": item.employee,
			"employee_name": item.employee_name,
			"date": item.date,
			"time": item.time,
			"log_type": '0' if item.log_type == "In" else '1',
			"trn_datetime": item.trn_datetime,
		}
		for item in doc.import_log_details
	]
		
	datalogs = attendance_log(docname, doctype, item_details)
		
	if datalogs['status'] == 'success':
		return {
			'status': 'success',
			'att_log': datalogs['message']['sorted_data'],
			'results': datalogs['message']['results']
		}
	else:
		frappe.throw(datalogs['message'])


def dat_function(docname, doctype, from_date, to_date, csv_file):
	file_doc = frappe.db.get_value("File", {"file_url": csv_file}, "name")
	if not file_doc:
		frappe.throw(_("File not found for the given URL: {0}").format(csv_file))
		
	content = frappe.get_doc("File", file_doc).get_content()
	from_date = datetime.strptime(from_date, '%Y-%m-%d')
	to_date = datetime.strptime(to_date, '%Y-%m-%d')
		
	lines = content.strip().split('\n')
	data = []
	for line in lines:
		columns = line.split('\t')
		if len(columns) != 6:
			frappe.log_error(message=line, title='File Format Error')
			continue
		
		date, time = columns[1].split(' ')
		record_date = datetime.strptime(date, '%Y-%m-%d')
		if not from_date <= record_date <= to_date:
			continue
		
		employee = frappe.db.get_value(
			"Employee", {'attendance_device_id': int(columns[0])}, ['name', 'employee_name'], as_dict=True
		)
		if employee:
			data.append({
				'biometric_id': int(columns[0]),
				'employee': employee['name'],
				'employee_name': employee['employee_name'],
				'date': date, 'time': time,
				'log_type': columns[3],
				'log_type_text': 'In' if columns[3] == "0" else 'Out',
				'trn_datetime': columns[1],
			})
		
	datalogs = attendance_log(docname, doctype, data)
	return {
		'status': 'success',
		'data_group': datalogs['results'],
		'dat_list': datalogs['sorted_data']
	}


def attendance_log(docname, doctype, data):
	for entry in data:
		entry["datetime"] = datetime.strptime(f"{entry['date']} {entry['time']}", "%Y-%m-%d %H:%M:%S")
		# x.employee, x.date, time_to_seconds(x.time)
	sorted_data = sorted(data, key=lambda x: (x["employee"], x["datetime"], x["log_type"]))
	filtered_data = []

	# Filter out logs within 5 minutes of each other
	for i, entry in enumerate(sorted_data):
		if i > 0 and entry['date'] == sorted_data[i-1]['date'] and entry['log_type'] == sorted_data[i-1]['log_type']:
			time_diff = entry['datetime'] - sorted_data[i-1]['datetime']
			if time_diff <= timedelta(minutes=5):
				continue
		filtered_data.append(entry)

	return {
		'status': 'success',
		'message': {
			'sorted_data': filtered_data,
			'results': len(filtered_data),
		}
	}


@frappe.whitelist()
def get_filtered_print(docname, filters=None):
    doc = frappe.get_doc('Import Logs', docname)
    if filters:
        filters = json.loads(filters)  # Parse the filter JSON if passed as a string
    return frappe.get_print('Import Logs', docname, print_format='Your Print Format', filters=filters)