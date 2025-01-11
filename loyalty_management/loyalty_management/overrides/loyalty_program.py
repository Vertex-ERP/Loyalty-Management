import frappe
from erpnext.accounts.doctype.loyalty_program.loyalty_program import LoyaltyProgram ,get_loyalty_program_details , get_loyalty_program_details_with_points
from frappe.utils import flt, today
from frappe import _




@frappe.whitelist()
def get_loyalty_program_details_with_points(
    customer,
    loyalty_program=None,
    expiry_date=None,
    company=None,
    silent=False,
    include_expired_entry=False,
    current_transaction_amount=0,
    current_transaction_qty=0,  # Updated to use quantity

):
    # frappe.msgprint("ppp")
    
    lp_details = get_loyalty_program_details(
        customer, loyalty_program, company=company, silent=silent
    )
    loyalty_program = frappe.get_doc("Loyalty Program", loyalty_program)
    lp_details.update(
        get_loyalty_details(customer, loyalty_program.name, expiry_date, company, include_expired_entry)
    )


    # Determine the field name for comparison based on the program
    based_on_field = "custom_min_qty_spent" if loyalty_program.custom_based_on == "Total Qty" else "min_spent"
    current_transaction_value=current_transaction_qty  if loyalty_program.custom_based_on == "Total Qty" else current_transaction_amount

    
    tier_spent_level = sorted(
        [d.as_dict() for d in loyalty_program.collection_rules],
        key=lambda rule: rule[based_on_field],  
        reverse=True,
    )
    
   
    
   

    for i, d in enumerate(tier_spent_level):
        if i == 0 or (lp_details.get(based_on_field.replace("min_", "total_"), 0) + current_transaction_value) <= d[based_on_field]:
            lp_details.tier_name = d.tier_name
            lp_details.collection_factor = d.collection_factor
        else:
            break

    return lp_details






def get_loyalty_details(
customer, loyalty_program, expiry_date=None, company=None, include_expired_entry=False
):
    if not expiry_date:
        expiry_date = today()

    filters = {
        "customer": customer,
        "loyalty_program": loyalty_program,
        "posting_date": ("<=", expiry_date),
    }

    if company:
        filters["company"] = company
    if not include_expired_entry:
        filters["expiry_date"] = (">=", expiry_date)

    # Fetch the entries from the database
    loyalty_entries = frappe.get_all(
        "Loyalty Point Entry",
        filters=filters,
        fields=["loyalty_points", "purchase_amount", "custom_purchase_qty"],
    )

    # Summing the fields programmatically
    total_loyalty_points = sum(entry.get("loyalty_points", 0) for entry in loyalty_entries)
    total_spent = sum(entry.get("purchase_amount", 0) for entry in loyalty_entries)
    total_qty_spent = sum(entry.get("custom_purchase_qty", 0) for entry in loyalty_entries)

    return {
        "loyalty_points": total_loyalty_points,
        "total_spent": total_spent,
        "custom_total_qty_spent": total_qty_spent,
    }
   


    






