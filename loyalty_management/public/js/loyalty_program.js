frappe.ui.form.on('Loyalty Program', {
    refresh: function(frm) {
        hide_standard_fields(frm);
        frm.events.set_field_options(frm);
    },
    validate(frm) {
		frm.set_df_property("custom_user_field", "reqd", !frm.doc.custom_for_assigned_users);
		frm.set_df_property("custom_condition", "reqd", frm.doc.custom_for_doc_event === "Custom");
	},
    // for_doc_event(frm) {
	// 	if (frm.doc.custom_for_assigned_users) {
	// 		frm.set_value("custom_for_assigned_users", !frm.doc.custom_for_doc_event === "New");
	// 	}
	// },

    custom_reference_doctype(frm) {
		
        frm.events.set_field_options(frm);
		
	},
	set_field_options(frm) {
		// sets options for field_to_check, user_field and multiplier fields
		// based on reference doctype
		const reference_doctype = frm.doc.custom_reference_doctype;
		if (!reference_doctype) return;

		frappe.model.with_doctype(reference_doctype, () => {
			const map_for_options = (df) => ({ label: df.label, value: df.fieldname });
			const fields = frappe.meta
				.get_docfields(frm.doc.custom_reference_doctype)
				.filter(frappe.model.is_value_type);

			const fields_to_check = fields.map(map_for_options);

			const user_fields = fields
				.filter(
					(df) =>
						(df.fieldtype === "Link" && df.options === "Customer")
				)
				.map(map_for_options)
;

			const multiplier_fields = fields
				.filter((df) => ["Int", "Float"].includes(df.fieldtype))
				.map(map_for_options);
               

			// blank option for the ability to unset the multiplier field
			// multiplier_fields.unshift(null);

			frm.set_df_property("custom_field_to_check", "options", fields_to_check);
			frm.set_df_property("custom_user_field", "options", user_fields);
			frm.set_df_property("custom_based_on", "options", multiplier_fields);
		});
	},
    
    
});
function hide_standard_fields(frm) {
    
	frm.fields_dict['collection_rules'].grid.toggle_display('min_spent', false);
    
}
