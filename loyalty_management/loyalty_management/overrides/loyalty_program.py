import frappe
from erpnext.accounts.doctype.loyalty_program.loyalty_program import LoyaltyProgram ,get_loyalty_program_details 
from frappe.utils import  today
from frappe import _
from frappe.core.doctype.user.user import get_enabled_users

from frappe.utils import add_days
from frappe.model import log_types
import datetime
from frappe.utils import now
from math import floor




class CustomLoyaltyProgram(LoyaltyProgram): 
    
    def eval_condition(self, doc):
        return self.custom_condition and frappe.safe_eval(self.custom_condition, None, {"doc": doc.as_dict()})

    def on_update(self):
        frappe.cache_manager.clear_doctype_map("Loyalty Program", self.custom_reference_doctype)

    def on_trash(self):
        frappe.cache_manager.clear_doctype_map("Loyalty Program", self.custom_reference_doctype)

    @frappe.whitelist()
    def get_item_loyalty_points(self, tier_name):
        loyalty_points = frappe.db.sql(
        """
        SELECT
            i.item_name AS parent_item,
            ilp.name,
            ilp.tier_name,
            ilp.loyalty_program,
            ilp.collection_factor
        FROM `tabItem Loyalty Point` ilp
        LEFT JOIN `tabItem` i ON ilp.parent = i.name
        WHERE ilp.tier_name = %(tier_name)s AND ilp.loyalty_program = %(loyalty_program)s
        """,
        values={"tier_name": tier_name, "loyalty_program": self.name},
        as_dict=True
    )

        # frappe.msgprint(f"Result with alias: {loyalty_points}")
        return loyalty_points

    

    def rule_condition_satisfied(self, doc):
        if self.custom_for_doc_event == "New":
            if self.custom_condition and not self.eval_condition(doc):
                return False
            # indicates that this was a new doc
            return doc.get_doc_before_save() is None
        if self.custom_for_doc_event == "Submit":
            return doc.docstatus.is_submitted()
        if self.custom_for_doc_event == "Cancel":
            return doc.docstatus.is_cancelled()
        if self.custom_for_doc_event == "Value Change":
            field_to_check = self.custom_field_to_check
            if not field_to_check:
                return False
            doc_before_save = doc.get_doc_before_save()
            # check if the field has been changed
            # if condition is set check if it is satisfied
            return (
                doc_before_save
                and doc_before_save.get(field_to_check) != doc.get(field_to_check)
                and (not self.custom_condition or self.eval_condition(doc))
            )

        if self.custom_for_doc_event == "Custom" and self.custom_condition:
            return self.eval_condition(doc)
        return False

    def get_item_collection_factor(self,item_code, tier_name):
        item_doc = frappe.get_doc("Item", item_code)

        # Ensure the child table exists
        if not hasattr(item_doc, "custom_loyalty_points"):
            frappe.throw(_("The Item Doctype does not have a custom_loyalty_points child table."))

        # Search for the matching tier in the child table
        for loyalty_point in item_doc.custom_loyalty_points:
            if loyalty_point.loyalty_program==self.name and  loyalty_point.tier_name == tier_name:
                return loyalty_point.collection_factor
            

    

    def apply(self, doc):
        # frappe.msgprint(f"apply {self.name}")
        #field is user_field in loyal program
        #if doc.[field] is equal name of program

        # current_time = now().split(" ")[1][:5]  # Extract "HH:MM"
        # current_time.split
        exists = frappe.db.exists(
        "Loyalty Point Entry",
        {
        "invoice": doc.name,
        "loyalty_points":   [">", -1],


        
        },
        )
        # frappe.msgprint(f"exist{exists}")
        if exists:
             return
        
        customer_program=frappe.db.get_value("Customer", doc.get(self.custom_user_field), "loyalty_program")
        if customer_program==self.name and self.custom_reference_doctype == doc.get("doctype"):
            # frappe.msgprint(f"true {self.name},{self.custom_based_on}")


            if self.rule_condition_satisfied(doc):
           
                lp_details=get_loyalty_program_details_with_points( customer=  doc.get(self.custom_user_field), loyalty_program=self.name,expiry_date=doc.creation,company=self.company,include_expired_entry=True )
                # frappe.msgprint(f"{lp_details.collection_factor}")
                # if doc.get(self.custom_based_on):#??
                #     frappe.msgprint("here1")
                    
                if not self.custom_based_on_item:#up 1 level
                    # frappe.msgprint("here0")
                    if doc.get(self.custom_based_on):
                                        
                        points=floor(doc.get(self.custom_based_on) /lp_details.collection_factor)
                        based_on_value=doc.get(self.custom_based_on)
                        # frappe.msgprint(f"points{points}")
                else:# in case it is based on item
                    #get the items child table and get distinct items with how many times the exist
                    #get thier lotlaty point details and compare
                    # calculate returned points
                    # frappe.msgprint("here")
                        
                    points = 0
                    based_on_value=0
                    # frappe.msgprint(f"{self.custom_table_based_on}")
                    items = doc.get(self.custom_table_based_on)
                    has_field = hasattr(items[0], self.custom_based_on) if items else False
                    # frappe.msgprint(f"has_qty_field {has_field,{items}}")
                    item_counts = {}
                    if has_field:
                        # frappe.msgprint("has_qty_field true")
                        for item in items:#calculate qty(should be chosen form desk)
                            increment_value = item.get(self.custom_based_on) 
                            
                        
                            item_code = item.get("item_code") 
                            if item_code in item_counts:
                                item_counts[item_code] += increment_value
                            else:
                                item_counts[item_code] = increment_value
                        # Loop through distinct items and calculate points for each
                        for item_code, count in item_counts.items():
                            # Fetch loyalty point details for the item
                            # lp_details = frappe.get_value("Loyalty Point Details", {"item_code": item_code}, ["collection_factor"])#???

                            if lp_details:
                                # Calculate points for this item based on its count and collection factor
                                #get collection factor from item
                                collection_factor=self.get_item_collection_factor(item_code, lp_details["tier_name"])
                                if collection_factor:
                                    points += floor(count / collection_factor)
                                    based_on_value+=count
                    # frappe.msgprint(f"item_counts{item_counts}")
                    else:
                        return
                if self.custom_max_points and points > self.custom_max_points:
                    points = self.custom_max_points
                    if not points:
                        return
                # frappe.msgprint(f"points{points}")
                

                # try:  
                creation_datetime = frappe.db.get_value(doc.doctype, {"name": doc.name}, "creation")

                creation_date = creation_datetime.date()
                
                doc = frappe.get_doc(
                    {
                        "doctype": "Loyalty Point Entry",
                        "company": lp_details.company,
                        "loyalty_program": lp_details.loyalty_program,
                        "loyalty_program_tier": lp_details.tier_name,
                        "customer": doc.get(self.custom_user_field),
                        "invoice_type": doc.doctype,
                        "invoice": doc.name,
                        "loyalty_points": points,
                        "custom_based_on_value": based_on_value,
                        "expiry_date": add_days(creation_date, lp_details.expiry_duration),
                        "posting_date": creation_date,
                    }
                ).insert()     
                    # frappe.msgprint(f"created:{doc.name}")         
                    
                # except Exception as e:
                #     self.log_error("Loyalty points failed")

                        
                    

                            
            
                
                # multiplier = 1

                # points = self.points
                # if self.custom_multiplier_field:
                #     multiplier = doc.get(self.custom_multiplier_field) or 1
                #     points = round(points * multiplier)
                #     max_points = self.custom_max_points
                #     if max_points and points > max_points:
                #         points = max_points

                # reference_doctype = doc.doctype
                # reference_name = doc.name
                # users = []
            
                # users = [doc.get(self.user_field)]
                # rule = self.name

                # # incase of zero as result after roundoff
            

            
        


@frappe.whitelist()
def get_loyalty_program_details_with_points(
    customer,
    loyalty_program=None,
    expiry_date=None,
    company=None,
    silent=False,
    include_expired_entry=False,
    # current_transaction_amount=0,
    # current_transaction_value=0.0 

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
    # based_on_field = "custom_min_qty_spent" if loyalty_program.custom_based_on == "Total Qty" else "min_spent" #min_value
    # current_transaction_value=current_transaction_qty  if loyalty_program.custom_based_on == "Total Qty" else current_transaction_amount

    
    tier_spent_level = sorted(
        [d.as_dict() for d in loyalty_program.collection_rules],
        key=lambda rule: rule.custom_min_value,  
        reverse=True,
    )
    
    

    
    # frappe.msgprint(f"lp_details.get('total_value', 0) {lp_details.get('total_value', 0)}")

    for i, d in enumerate(tier_spent_level):

        if i == 0 or (lp_details.get("total_value", 0) ) <= d["custom_min_value"]:
            lp_details.tier_name = d.tier_name
            lp_details.collection_factor = d.collection_factor
        else:
            break


    return lp_details



def get_loyalty_details(
customer, loyalty_program, expiry_date=None, company=None, include_expired_entry=False
):
    if not expiry_date:
        # frappe.msgprint("no exp date")
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
    # frappe.msgprint(f"filters {filters}")


    # Fetch the entries from the database
    loyalty_entries = frappe.get_all(
        "Loyalty Point Entry",
        filters=filters,
        fields=["loyalty_points", "custom_based_on_value"],
    )
    # frappe.msgprint(f"loyalty_entries {loyalty_entries}")

    total_loyalty_points = sum(entry.get("loyalty_points", 0) for entry in loyalty_entries)
    total= sum(entry.get("custom_based_on_value", 0) for entry in loyalty_entries)
   

    return {
        "loyalty_points": total_loyalty_points,
        "total_value": total,
        # "total_spent": total_spent,
        # "custom_total_qty_spent": total_qty_spent,

    }


# this method is called on_change of the document
#it applies changes into points based on the rules defined
def process_loyalty_points(doc, state):
    # frappe.msgprint("overiden by loyalty management")
    # frappe.msgprint("rty")
    # if (
    #     frappe.flags.in_patch
    #     or frappe.flags.in_install
    #     or frappe.flags.in_migrate
    #     or frappe.flags.in_import
    #     or frappe.flags.in_setup_wizard
    #     or doc.doctype in log_types
    # ):
       
    #     return

    # if not is_energy_point_enabled():
    # 	return
    #get doc info before save
    old_doc = doc.get_doc_before_save()

    # check if doc has been cancelled
    if old_doc and old_doc.docstatus.is_submitted() and doc.docstatus.is_cancelled():
        return revert_points_for_cancelled_doc(doc)
    
    # frappe.msgprint("apply points")
    # for d in frappe.cache_manager.get_doctype_map(
    #     "Loyalty Program", doc.doctype, dict(custom_reference_doctype=doc.doctype, custom_enabled=1)
    # ):
    #     # program = frappe.get_doc("Loyalty Program", d.get("name"))
    #     frappe.msgprint(f"Program: ")
    programs = frappe.cache_manager.get_doctype_map(
    "Loyalty Program", doc.doctype
    )
#     programs_ = frappe.get_all(
#     "Loyalty Program", 
    
#     fields=["*"]
# )

    # frappe.msgprint(f"programs {programs}")
    
    

    if programs:
        # frappe.msgprint(f"No programs found for Doctype: {doc.doctype}")
        for d in programs:  
            # frappe.msgprint(f"Program Found: {d.get('name')}")



            frappe.get_doc("Loyalty Program", d.get("name")).apply(doc)
    
        



def revert_points_for_cancelled_doc(doc):
    # frappe.msgprint("canceled")

    entries = frappe.get_all(
        "Loyalty Point Entry",
        {"invoice_type": doc.doctype, "invoice": doc.name},
    )
    # frappe.msgprint(f"entries{entries}")
    for entry in entries:
        reference_log = frappe.get_doc("Loyalty Point Entry", entry.name)
        reference_log.revert(_("Reference document has been cancelled"), ignore_permissions=True)


# def get_energy_point_doctypes():
# 	return [
# 		d.reference_doctype
# 		for d in frappe.get_all("Energy Point Rule", ["reference_doctype"], {"enabled": 1})
# 	]


def is_eligible_user(user):
    """Checks if user is eligible to get energy points"""
    enabled_users = get_enabled_users()
    return user and user in enabled_users and user != "Administrator"


@frappe.whitelist()
def get_item_loyalty_points(loyalty_program):
     # Query the child table directly
        loyalty_points = frappe.get_all(
            "Item Loyalty Point",
            filters={"loyalty_program": loyalty_program},
            fields=["name", "parent", "tier_name", "collection_factor"]  # Specify the fields you need
        )
        return loyalty_points





    






