frappe.ui.form.on('Loyalty Program', {
    refresh: function(frm) {
        hide_standard_fields(frm);
        frm.events.set_field_options(frm);
		frm.events.set_items_based_prop(frm);
		toggleColumns(frm,["collection_factor"],"collection_rules")

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
		frm.events.set_items_based_prop(frm);

		
	},
	
	custom_based_on_item(frm){
	    toggleColumns(frm,["collection_factor"],"collection_rules")
	   
	   
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
				.map(map_for_options);
				

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

	set_items_based_prop(frm) {
		if (frm.doc.custom_reference_doctype) {
			// Load the metadata of the referenced Doctype
			frappe.model.with_doctype(frm.doc.custom_reference_doctype, () => {
				// Check if the 'items' field exists in the DocType
				const has_items_field = frappe.meta.has_field(frm.doc.custom_reference_doctype, 'items');
	
				if (has_items_field) {
					// frappe.msgprint("has")
					frm.set_df_property("custom_based_on_item", "hidden", false);
					
				} else {
					// frappe.msgprint("has no")
					frm.set_df_property("custom_based_on_item", "hidden", true);
					frm.set_value("custom_based_on_item", false);
				}
			});
		}
	},
	set_item_details_prop(frm) {
		if (frm.doc.custom_based_on_item) {
			frappe.msgprint("here")
			frm.set_df_property("custom_item_point_details", "hidden", false);
			frm.set_df_property("custom_add_item", "hidden", false);
			// frm.set_df_property("collection_factor", "hidden", true);
			
		}
		else{
			frappe.msgprint("here2")
			// frm.set_df_property("custom_item_details", "hidden", true);
			// frm.set_df_property("collection_factor", "hidden", false);
		}
	}
	
	

    
});
function hide_standard_fields(frm) {
    
	frm.fields_dict['collection_rules'].grid.toggle_display('min_spent', false);
    
}

frappe.ui.form.on("Loyalty Program Collection", "form_render", function(frm, cdt, cdn){
    // frappe.msgprint("ppp")
    const row_doc = locals[cdt][cdn];
      frappe.call({
                method: 'get_item_loyalty_points',
                doc:frm.doc,
                args: {
                    tier_name: row_doc.tier_name,
                    
                },
                callback: function(r) {
                    if (r.message && r.message.length) {
                       
                        const items = r.message;
                        //  frappe.msgprint("here2"+items)

                        // Generate HTML table
                        let html = `<table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Collection Factor</th>
                                </tr>
                            </thead>
                            <tbody>`;
                        

                        items.forEach(item => {
                            html += `<tr>
                                <td>${item.parent_item}</td>
                                <td>${item.collection_factor}</td>
                            </tr>`;
                        });

                        html += `</tbody></table>`;
                        

                        // Assign the table to the HTML field
                         wrapper = frm.fields_dict[row_doc.parentfield].grid.grid_rows_by_docname[cdn].grid_form.fields_dict['custom_item_point_details'].wrapper
$(html).appendTo(wrapper);
   

                    } else {
                         wrapper = frm.fields_dict[row_doc.parentfield].grid.grid_rows_by_docname[cdn].grid_form.fields_dict['custom_item_point_details'].wrapper
$(`<p>No items found for this tier.</p>`).appendTo(wrapper);
                       
                    }
                }
            });

});


function toggleColumns(frm, fields, table) {
   
    let grid = frm.get_field(table).grid;
    
    
    var hidden_val=frm.doc.custom_based_on_item
    
    for (let field of fields) {
        grid.fields_map[field].hidden = hidden_val;
        grid.update_docfield_property(
                        field,
                        'hidden',
                        hidden_val // Options should be newline-separated
                    );
    }
    
  
    // frappe.msgprint("herer")
    
     
    grid.visible_columns = undefined;
    grid.setup_visible_columns();
    
    grid.header_row.wrapper.remove();
    delete grid.header_row;
    grid.make_head();
    
    for (let row of grid.grid_rows) {
        if (row.open_form_button) {
            row.open_form_button.parent().remove();
            delete row.open_form_button;
        }
        
        for (let field in row.columns) {
            if (row.columns[field] !== undefined) {
                row.columns[field].remove();
            }
        }
        delete row.columns;
        row.columns = [];
        row.render_row();
    }
     frm.fields_dict['collection_rules'].grid.update_docfield_property(
                        'custom_item_point_details',
                        'hidden',
                        !frm.doc.custom_based_on_item
                    );
    
    // frappe.msgprint("herer")
}


