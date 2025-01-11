# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


import frappe
from frappe.utils import flt
from erpnext.accounts.doctype.loyalty_program.loyalty_program import get_loyalty_program_details_with_points


def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Customer", "fieldname": "customer_name", "fieldtype": "Link", "options": "Customer", "width": 200},
        
        {"label": "Program", "fieldname": "loyalty_program", "fieldtype": "Data", "width": 200},
        {"label": "Tier", "fieldname": "tier_name", "fieldtype": "Data", "width": 200},
        {"label": "Loyalty Points", "fieldname": "loyalty_points", "fieldtype": "Int", "width": 150},
        # {"label": "Total Quantity", "fieldname": "total_qty", "fieldtype": "Float", "width": 150},
        # {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    company = filters.get("company")
    loyalty_program = filters.get("loyalty_program")

    if not company:
        frappe.throw("Please select a company to generate the report.")

    # # Fetch customers with loyalty points, tier, total qty, and total amount
    # customers = frappe.db.sql("""
    #     SELECT
    #         c.name AS customer,
    #         COALESCE(lp.loyalty_points, 0) AS loyalty_points,
    #         lt.tier_name AS tier,
    #         SUM(si_item.qty) AS total_qty,
    #         SUM(si_item.base_net_amount) AS total_amount
    #     FROM
    #         `tabCustomer` c
    #     LEFT JOIN
    #         `tabLoyalty Program` lp ON c.loyalty_program = lp.name
    #     LEFT JOIN
    #         `tabLoyalty Tier` lt ON c.tier = lt.name
    #     LEFT JOIN
    #         `tabSales Invoice` si ON si.customer = c.name AND si.company = %s AND si.docstatus = 1
    #     LEFT JOIN
    #         `tabSales Invoice Item` si_item ON si_item.parent = si.name
    #     GROUP BY
    #         c.name
    # """, (company,), as_dict=True)
    
	
    all_customers=get_customers_with_sales_invoices(company,loyalty_program)
    
    customers_loyalty=get_customers_loyalty_points(all_customers)
    # frappe.msgprint(f"customers{customers_loyalty}")


    return customers_loyalty



#Get Customers with Sales Invoices related the chosen company
def get_customers_with_sales_invoices(company,loyalty_program=None):
    if not company:
        frappe.throw("Please provide a company.")

    # Fetch all customers with sales invoices in the specified company
    sales_invoice_customers = frappe.db.get_all(
        "Sales Invoice",
        filters={"company": company, "docstatus": 1},
        pluck="customer"
    )

    # Remove duplicates
    sales_invoice_customers = list(set(sales_invoice_customers))
    customer_filters = {"name": ["in", sales_invoice_customers]}
    if loyalty_program:
        customer_filters["loyalty_program"] = loyalty_program

    # Fetch customer details
    customers=frappe.db.get_all(
		"Customer",
		filters=customer_filters,
		fields=["name", "customer_name","loyalty_program"]
	)
    

    return customers

def get_customers_loyalty_points(customers):
    # frappe.msgprint("in get points")
   
    # Prepare results
    results = []

    for customer in customers:
        # frappe.msgprint(f"{customer.name}")
        # Call the loyalty program method for each customer
        loyalty_details = get_loyalty_program_details_with_points(customer.name,loyalty_program=customer.loyalty_program)
        # frappe.msgprint(f"loyalty_details {loyalty_details}")
        
        # # Add details to results
        results.append({
            "customer_name": customer.name,
            "loyalty_program": customer.loyalty_program,
            "loyalty_points": loyalty_details.get("loyalty_points"),
            "tier_name": loyalty_details.get("tier_name"),
			# "total_amount": loyalty_details.get("total_spent"),
            # "total_qty": loyalty_details.get("custom_total_qty_spent"),
              
        })

    return results


