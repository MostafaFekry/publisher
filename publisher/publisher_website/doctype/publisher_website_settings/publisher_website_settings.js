// Copyright (c) 2020, Alzad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Publisher Website Settings', {
	 refresh: function(frm) {
     frm.trigger('set_update_publisher_app');
 		 frm.trigger('set_add_examples_data');
	 },
  onload: function(frm) {
    //get query select item group
  		frm.fields_dict['publication_item_group'].get_query = function(doc,cdt,cdn) {
  			return{
  				filters:[
  					['Item Group', 'is_group', '=', 1],
  					['Item Group', 'show_in_website', '=', 1]
  				]
  			}
  		}

  },
  set_update_publisher_app(frm) {
    if ( !frm.doc.all_data_added_to_publisher  && !frm.doc.example_data_updated && !frm.is_dirty()) {
      frm.add_custom_button(__('Update Publisher app'), () => {
        frm.call('update_publisher_app').then(() => frm.trigger('refresh'));
      });
    }
  },
  set_add_examples_data(frm) {
    if ( frm.doc.all_data_added_to_publisher  && !frm.doc.example_data_updated && !frm.is_dirty()) {
      frm.add_custom_button(__('Add examples data'), () => {
        frm.call('add_examples_data').then(() => frm.trigger('refresh'));
      });
    }
  }

});
