// frappe.ui.form.on('Item Loyalty Point', {
//     refresh:function(frm){
//         frappe.msgprint("A")
//     },
//     loyalty_program: function(frm) {
//         // Get the selected loyalty program
//         const loyalty_program = frm.doc.loyalty_program;
        
//         // If there's no loyalty program selected, do nothing
//         if (!loyalty_program) {
//             return;
//         }

//         // Fetch the tiers associated with the selected loyalty program
//         frappe.call({
//             method: 'frappe.client.get',
//             args: {
//                 doctype: 'Loyalty Program',
//                 name: loyalty_program
//             },
//             callback: function(response) {
//                 const loyalty_program_doc = response.message;
                
//                 // If the loyalty program is found, extract the tiers
//                 if (loyalty_program_doc && loyalty_program_doc.tiers) {
//                     const tiers = loyalty_program_doc.tiers;

//                     // Loop through the rows in Item Loyalty Point table
//                     frm.doc.item_loyalty_points.forEach(row => {
//                         // Get the select field (tier) for each row
//                         const select_field = frm.fields_dict.item_loyalty_points.grid.get_field('tier');
                        
//                         // Update the options for the select field
//                         if (select_field) {
//                             select_field.options = tiers.join('\n');  // Join the tiers into a string separated by new lines
//                         }
//                     });

//                     // Refresh the child table to reflect the changes
//                     frm.refresh_field('item_loyalty_points');
//                 }
//             }
//         });
//     }
// });
