frappe.ui.form.on('Loyalty Program', {
    refresh: function(frm) {
        toggle_minimum_total_column(frm);
    },

    custom_based_on: function(frm) {
        toggle_minimum_total_column(frm);
    }
    
});
function toggle_minimum_total_column(frm) {
    
    if (frm.doc.custom_based_on === 'Total Qty') {
    // Hide the 'minimum_total' column in the 'collection_rules' child table
    frm.fields_dict['collection_rules'].grid.toggle_display('min_spent', false);
    frm.fields_dict['collection_rules'].grid.toggle_display('custom_min_qty_spent', true);
} else {
    // frappe.msgprint("total amonut")
    // Show the 'minimum_total' column if the condition is not met
    frm.fields_dict['collection_rules'].grid.toggle_display('min_spent', true);
    frm.fields_dict['collection_rules'].grid.toggle_display('custom_min_qty_spent', false);
}
}
