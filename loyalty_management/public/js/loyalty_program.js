frappe.ui.form.on('Loyalty Program', {
    refresh: function(frm) {
        hide_standard_fields(frm);
		// if(frm.doc.custom_based_on_item){
		// 	frm.events.set_item_table(frm);}
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
	
	custom_based_on_item(frm) {
	  
		
		frm.events.set_field_options(frm);
		toggleColumns(frm,["collection_factor"],"collection_rules")
	   
		
	},
	custom_table_based_on(frm){
		frm.events.set_field_options(frm);
	//     const map_for_options = (df) => ({ label: df.label, value: df.fieldname });
	//     // frappe.msgprint("here")
	//       const table_fields = frappe.meta
	// 			.get_docfields(frm.doc.custom_table_based_on)
	// 			.filter(frappe.model.is_value_type);
	// 			multiplier_fields = table_fields
	// 			.filter((df) => ["Int", "Float"].includes(df.fieldtype))
	// 			.map(map_for_options);
	// frm.set_df_property("custom_based_on", "options", multiplier_fields);
	},
	

    custom_reference_doctype(frm) {
		// if(frm.doc.custom_based_on_item){
		// frm.events.set_item_table(frm);}
        frm.events.set_field_options(frm);
		frm.events.set_items_based_prop(frm);

		
	},
	
	// custom_based_on_item(frm){
	   
	   
	// },

	set_field_options(frm) {
		// frappe.msgprint("set_field_options")
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

			multiplier_fields=[]
			if(!frm.doc.custom_based_on_item){
				// frappe.msgprint("not")
			multiplier_fields = fields
				.filter((df) => ["Int", "Float","Currency"].includes(df.fieldtype))
				.map(map_for_options);
			}
			else{
				frm.events.set_item_table(frm);


								// Get the selected fieldname from the dropdown
				let selected_fieldname = frm.doc.custom_table_based_on; // This now stores the actual fieldname

				// Find the matching child table DocType based on fieldname
				frappe.model.with_doctype(frm.doc.custom_reference_doctype, () => {
					let childTableMeta = frappe.get_meta(frm.doc.custom_reference_doctype).fields
						.find(df => df.fieldtype === "Table" && df.fieldname === selected_fieldname); // Match by fieldname

					console.log("Selected Child Table Meta:", childTableMeta);

					if (childTableMeta) {
						let child_table_doctype = childTableMeta.options; // Get actual DocType name
						console.log("Actual Child Table DocType:", child_table_doctype);

						// Now fetch the fields from the correct DocType
						const table_fields = frappe.meta
							.get_docfields(child_table_doctype)
							.filter(frappe.model.is_value_type);

						// Filter numeric fields & format as {label, value}
						multiplier_fields = table_fields
							.filter(df => ["Int", "Float", "Currency"].includes(df.fieldtype))
							.map(map_for_options);

						console.log("Multiplier Fields:", multiplier_fields);

						// // ✅ Set the dropdown options for the target field (e.g., `custom_multiplier_field`)
						// frm.set_df_property("custom_multiplier_field", "options", multiplier_fields);
					} else {
						console.warn("No matching child table found for fieldname:", selected_fieldname);
					}
				});


							// frm.set_df_property("custom_based_on", "options", multiplier_fields);
				

			}


			frm.set_df_property("custom_field_to_check", "options", fields_to_check);
			frm.set_df_property("custom_user_field", "options", user_fields);
			frm.set_df_property("custom_based_on", "options", multiplier_fields);
			// console.log("selected items"+multiplier_fields)
			// frm.set_df_property("custom_child_table_with_item", "options", childTablesWithItemLink); // Add child tables

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
			// frappe.msgprint("here")
			frm.set_df_property("custom_item_point_details", "hidden", false);
			frm.set_df_property("custom_add_item", "hidden", false);
			// frm.set_df_property("collection_factor", "hidden", true);
			
		}
		else{
			// frappe.msgprint("here2")
			// frm.set_df_property("custom_item_details", "hidden", true);
			// frm.set_df_property("collection_factor", "hidden", false);
		}
	},
	set_item_table(frm) {
		frappe.model.with_doctype(frm.doc.custom_reference_doctype, () => {
			let childTableOptions = []; // Store field labels & values
			
			// Fetch all child table fields from the reference Doctype
			frappe.get_meta(frm.doc.custom_reference_doctype).fields
				.filter(df => df.fieldtype === "Table") // Ensure it's a child table
				.forEach(df => {
					let childTable = df.options; // Get child table DocType name
					let fieldLabel = df.label;   // Get field title (label)
					let fieldname = df.fieldname; // Get actual fieldname
	
					// Get fields of the child table Doctype
					let childFields = frappe.meta.get_docfields(childTable);
	
					// Check if any field is a "Link" type and linked to "Item"
					let hasItemLink = childFields.some(field => field.fieldtype === "Link" && field.options === "Item");
	
					if (hasItemLink) {
						// Store both label and fieldname so we can retrieve the fieldname later
						childTableOptions.push({ label: fieldLabel, value: fieldname });
					}
				});
	
			// Set the dropdown options using both field labels and values
			frm.set_df_property("custom_table_based_on", "options", childTableOptions.map(opt => opt));
	
			// Debugging log (optional)
			console.log("Child Tables with Link to Item (Field Titles & Fieldnames):", childTableOptions);
		});
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


