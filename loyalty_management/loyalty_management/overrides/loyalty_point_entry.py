import frappe

from erpnext.accounts.doctype.loyalty_point_entry.loyalty_point_entry import LoyaltyPointEntry

from frappe import _

class CustomLoyaltyPointEntry(LoyaltyPointEntry):
    

    @frappe.whitelist()
    def revert(self, reason, ignore_permissions=False):
        if not ignore_permissions:
            frappe.only_for("System Manager")

        # if self.type != "Auto":
        #     frappe.throw(_("This document cannot be reverted"))

        if self.get("reverted"):
            return

        self.custom_reverted = 1
        self.save(ignore_permissions=True)
        # frappe.msgprint(f"entry{self.company}")

        doc = frappe.get_doc(
                        {
                            "doctype": "Loyalty Point Entry",
                            "company": self.company,
                            "loyalty_program": self.loyalty_program,
                            "loyalty_program_tier": self.loyalty_program_tier,
                            "customer": self.customer,
                            "invoice_type": self.invoice_type,
                            "invoice": self.invoice,
                            "loyalty_points": - self.loyalty_points,
                             "reason": reason,
                            "custom_based_on_value": self.custom_based_on_value,
                
                            "expiry_date": self.expiry_date,
                            "posting_date": self.posting_date,
                        }
                    ).insert()

       