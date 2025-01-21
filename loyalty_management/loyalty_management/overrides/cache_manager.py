import frappe
from frappe.cache_manager import doctypes_for_mapping

def extend_doctype_mapping():
    
    doctypes_for_mapping.add("Loyalty Program")