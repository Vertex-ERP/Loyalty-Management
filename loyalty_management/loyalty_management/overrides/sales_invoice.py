import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from frappe.utils import add_days, cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate
from loyalty_management.loyalty_management.overrides.loyalty_program import (
    get_loyalty_program_details_with_points,
	
	
)


class CustomSalesInvoice(SalesInvoice):

    @frappe.whitelist()
    def get_returned_qty(self):
        from frappe.query_builder.functions import Sum

        doc = frappe.qb.DocType(self.doctype)
        returned_qty = (
            frappe.qb.from_(doc)
            .select(Sum(doc.total_qty))
            .where((doc.docstatus == 1) & (doc.is_return == 1) & (doc.return_against == self.name))
        ).run()

        return abs(returned_qty[0][0]) if returned_qty[0][0] else 0



    # collection of the loyalty points, create the ledger entry for that.
    def make_loyalty_point_entry(self):
        # frappe.msgprint("from custom sales invoice")
       
            

        returned_amount = self.get_returned_amount()
            

        
        returned_qty = self.get_returned_qty()
        # frappe.msgprint(f"returned_qty {returned_qty}")
        current_amount = flt(self.grand_total) - cint(self.loyalty_amount)
        eligible_amount = current_amount - returned_amount
        eligible_qty = self.total_qty - returned_qty

        lp_details = get_loyalty_program_details_with_points(
            self.customer,
            company=self.company,
            current_transaction_amount=current_amount,#what is it used for?
            current_transaction_qty=returned_qty,#new oa
            
            loyalty_program=self.loyalty_program,
            expiry_date=self.posting_date,
            include_expired_entry=True,
        )
        # frappe.msgprint(f"lp_details {lp_details}")
        if (
            lp_details
            and getdate(lp_details.from_date) <= getdate(self.posting_date)
            and (not lp_details.to_date or getdate(lp_details.to_date) >= getdate(self.posting_date))
        ):

            collection_factor = lp_details.collection_factor if lp_details.collection_factor else 1.0
            if lp_details.custom_based_on=="Total Qty":
           
                points_earned = cint(eligible_qty / collection_factor)
            else:
                points_earned = cint(eligible_amount / collection_factor)

            doc = frappe.get_doc(
                {
                    "doctype": "Loyalty Point Entry",
                    "company": self.company,
                    "loyalty_program": lp_details.loyalty_program,
                    "loyalty_program_tier": lp_details.tier_name,
                    "customer": self.customer,
                    "invoice_type": self.doctype,
                    "invoice": self.name,
                    "loyalty_points": points_earned,
                    "purchase_amount": eligible_amount if lp_details.custom_based_on!="Total Qty" else 0,
                    "custom_purchase_qty":eligible_qty  if lp_details.custom_based_on=="Total Qty" else 0,
                    "expiry_date": add_days(self.posting_date, lp_details.expiry_duration),
                    "posting_date": self.posting_date,
                }
            )
            doc.flags.ignore_permissions = 1
            doc.save()
            self.set_loyalty_program_tier()

