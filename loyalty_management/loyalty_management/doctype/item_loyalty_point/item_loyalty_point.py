# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ItemLoyaltyPoint(Document):
		
	@frappe.whitelist()
	def get_item_loyalty_points(tier_name, loyalty_program):
		# Fetch all documents of the Item Loyalty Point doctype with the given conditions
		loyalty_points = frappe.db.get_list(
			'Item Loyalty Point', 
			filters={
				'tier_name': tier_name, 
				'loyalty_program': loyalty_program
			},
			fields=['parent', 'tier_name', 'loyalty_program', 'collection_factor']  # Adjust fields as necessary
		)
		frappe.msgptint(loyalty_points)
		return loyalty_points

