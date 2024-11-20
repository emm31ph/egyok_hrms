import os
import click
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.desk.page.setup_wizard.install_fixtures import (
    _,  # NOTE: this is not the real translation function
)

import json
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.installer import update_site_config

def after_install():
    make_fixtures()

def before_uninstall():
    delete_custom_fields(get_custom_fields())
    
def after_app_install(app_name): 
    create_custom_fields(get_custom_fields(), ignore_validate=True)

def before_app_uninstall(app_name): 
    pass

def get_custom_fields():
    field_config = {
        "Employee": [
            {"fieldname": "shift_type", "fieldtype": "Link", "label": _("Shift Type"), "no_copy": 1,"reqd":1,  "insert_after": "holiday_list"}
        ],
    }
    
    return field_config

def delete_custom_fields(custom_fields: dict):
    for doctype, fields in custom_fields.items():
        frappe.db.delete(
            "Custom Field",
            {
                "fieldname": ("in", [field["fieldname"] for field in fields]),
                "dt": doctype,
            },
        )

        frappe.clear_cache(doctype=doctype)


def make_fixtures():
    records = [
        ### Employment Type
        # {"doctype": "Employment Type", "employee_type_name": _("Full-time")},
        # {"doctype": "Employment Type", "employee_type_name": _("Part-time")},
        # {"doctype": "Employment Type", "employee_type_name": _("Probation")},
        # {"doctype": "Employment Type", "employee_type_name": _("Contract")},
        # {"doctype": "Employment Type", "employee_type_name": _("Commission")},
        # {"doctype": "Employment Type", "employee_type_name": _("Piecework")},
        # {"doctype": "Employment Type", "employee_type_name": _("Intern")},
        # {"doctype": "Employment Type", "employee_type_name": _("Apprentice")},
    ]
    make_records(records)
