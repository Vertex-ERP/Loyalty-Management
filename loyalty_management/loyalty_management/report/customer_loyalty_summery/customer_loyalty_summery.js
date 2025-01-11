// Copyright (c) 2025, Yemen Frappe and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Loyalty Summery"] = {
	"filters": [

		
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1
        },

		{
            "fieldname": "loyalty_program",
            "label": __("Loyalty Program"),
            "fieldtype": "Link",
            "options": "Loyalty Program",
            
        }
    
	]
};

// frappe.query_reports["Customer Loyalty Summary"] = {
//     "filters": [
//         {
//             "fieldname": "company",
//             "label": __("Company"),
//             "fieldtype": "Link",
//             "options": "Company",
//             "reqd": 1
//         }
//     ]
// };

