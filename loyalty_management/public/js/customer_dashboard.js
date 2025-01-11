frappe.ui.form.on('Customer', {
    refresh: function(frm) {
        // Override the existing set_party_dashboard_indicators function
        frappe.require('erpnext/public/js/utils.js', function() {
            erpnext.utils.set_party_dashboard_indicators = function(frm) {
                if (frm.doc.__onload && frm.doc.__onload.dashboard_info) {
                    frappe.msgprint("from custom js")
                    var company_wise_info = frm.doc.__onload.dashboard_info;

                    // if (company_wise_info.length > 1) {
                    //     company_wise_info.forEach(function(info) {
                    //         erpnext.utils.add_indicator_for_multicompany(frm, info);
                    //     });
                    // }
                    
                    // else if (company_wise_info.length === 1) {
                    //     frm.dashboard.add_indicator(__('Annual Billing: {0}',
                    //         [format_currency(company_wise_info[0].billing_this_year, company_wise_info[0].currency)]), 'blue');
                    //     frm.dashboard.add_indicator(__('Total Unpaid: {0}',
                    //         [format_currency(company_wise_info[0].total_unpaid, company_wise_info[0].currency)]),
                            
                    //     company_wise_info[0].total_unpaid ? 'orange' : 'green');
                    //     frm.dashboard.add_indicator(__('Total Qty Purchased: {0}',
                    //         [(company_wise_info[0].total_qty, company_wise_info[0].currency)]),'purple');

                    //     if (company_wise_info[0].loyalty_points) {
                    //         frm.dashboard.add_indicator(__('Loyalty Points: {0}',
                    //             [company_wise_info[0].loyalty_points]), 'blue');
                    //     }

                    //     // Add the custom indicator for total_qty
                    //     if (company_wise_info[0].total_qty) {
                    //         frm.dashboard.add_indicator(__('Total Quantity: {0}',
                    //             [company_wise_info[0].total_qty]), 'purple');
                    //     }
                    // }
                }
            };
        });
    }
});
