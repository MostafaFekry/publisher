// Copyright (c) 2020, Alzad and contributors
// For license information, please see license.txt

frappe.ui.form.on('Website Theme Settings', {
	refresh(frm) {
		frm.clear_custom_buttons();
		frm.toggle_display(["module", "custom"], !frappe.boot.developer_mode);

		frm.trigger('setup_configure_theme');
		frm.trigger('set_default_theme_button_and_indicator');

		if (!frm.doc.custom && !frappe.boot.developer_mode) {
			frm.set_read_only();
			frm.disable_save();
		} else {
			frm.enable_save();
		}
	},

	setup_configure_theme(frm) {
		frm.add_custom_button(__('Configure Theme'), () => {
			const d = new frappe.ui.Dialog({
				title: __('Configure Theme'),
				fields: [
					{
						label: __('Theme Colors'),
						fieldtype: 'Section Break',
					},
					{
						label: __('Primary Color'),
						fieldtype: 'Color',
						fieldname: 'primary_color'
					},
					{
						label: __('Secondary Color'),
						fieldtype: 'Color',
						fieldname: 'secondary_color'
					},
					{
						label: __('Tertiary Color'),
						fieldtype: 'Color',
						fieldname: 'tertiary_color'
					},
					{
						label: __('Quaternary Color'),
						fieldtype: 'Color',
						fieldname: 'quaternary_color'
					},
					{
						label: __('Misc'),
						fieldtype: 'Section Break',
					},
					{
						label: __('Navbar Style'),
						fieldtype: 'Select',
						fieldname: 'navbar_style',
						options: [
							'Light',
							'Dark'
						],
						default: 'Light'
					},
					{
						label: __('Rounded Corners'),
						fieldtype: 'Check',
						fieldname: 'enable_rounded',
						default: 1
					},
				],
				primary_action: (values) => {
					frm.set_value('theme_json', JSON.stringify(values));
					frm.events.set_theme_from_config(frm, values);
					d.hide();
				}
			});

			if (frm.doc.theme_json) {
				d.set_values(JSON.parse(frm.doc.theme_json));
			}
			d.show();
		});
	},

	set_default_theme_button_and_indicator(frm) {
		frappe.db.get_single_value('Publisher Website Settings', 'website_theme_settings')
			.then(value => {
				if (value === frm.doc.name) {
					frm.page.set_indicator(__('Default Theme'), 'green');
				} else {
					frm.page.clear_indicator();
					// show set as default button
					if (!frm.is_new() && !frm.is_dirty()) {
						frm.add_custom_button(__('Set as Default Theme'), () => {
							frm.call('set_as_default').then(() => frm.trigger('refresh'));
						});
					}
				}
			});
	},

	set_theme_from_config(frm, config) {
		const {
			primary_color,
      secondary_color,
      tertiary_color,
      quaternary_color,
			navbar_style,
			enable_rounded
		} = config;

		let scss_lines = [];
		let js_lines = [];
    scss_lines.push(
			`@import "publisher/public/master/scss/variables";`,
			'\n'
		);
		if (!(Boolean(enable_rounded))) {
			scss_lines.push(
				`$border-radius: 0;`
			);
		}
		if (primary_color) {
			scss_lines.push(
				`$color-primary: ${primary_color};`
			);
		}
    if (secondary_color) {
			scss_lines.push(
				`$color-secondary: ${secondary_color};`
			);
		}
    if (tertiary_color) {
			scss_lines.push(
				`$color-tertiary: ${tertiary_color};`
			);
		}
    if (quaternary_color) {
			scss_lines.push(
				`$color-quaternary: ${quaternary_color};`
			);
		}



		if (navbar_style === 'Dark') {
			if (!(frm.doc.js || '').includes(`.addClass('navbar-dark bg-dark')`)) {
				js_lines.push(
					`frappe.ready(() => {`,
					`\t$('.navbar').removeClass('navbar-light bg-white').addClass('navbar-dark bg-dark')`,
					`})`
				);
			}
		}

		scss_lines.push(
			`@import "publisher/public/master/scss/skin";`,
			'\n'
		);

		// set scss
		frm.set_value('theme_scss', scss_lines.join('\n'));

		// set js
		const js = frm.doc.js || '';
		frm.set_value('js', js_lines.join('\n') + js);
	}
});
