// Copyright (c) 2020, Alzad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Website Header Design', {
	 refresh: function(frm) {
 		frm.trigger('set_default_header_button_and_indicator');
	 },
  set_default_header_button_and_indicator(frm) {
		frappe.db.get_single_value('Publisher Website Settings', 'website_header_design')
			.then(value => {
				if (value === frm.doc.name) {
					frm.page.set_indicator(__('Default Header Design'), 'green');
				} else {
					frm.page.clear_indicator();
					// show set as default button
					if (!frm.is_new() && !frm.is_dirty()) {
						frm.add_custom_button(__('Default Header Design'), () => {
							frm.call('set_as_default').then(() => frm.trigger('refresh'));
						});
					}
				}
			});
	}
});
