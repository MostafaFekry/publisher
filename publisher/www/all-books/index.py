import frappe
from frappe.utils import cint
from publisher.publisher.product_configurator.utils import (get_products_for_website, get_product_settings,
	get_field_filter_data, get_attribute_filter_data,get_products_for_website_count)

sitemap = 1

def get_context(context):
	doc = frappe.get_cached_doc('Publisher Website Settings')
	context.title = doc.all_books_page_title or "Books"
	context.all_books_column_value = cint(12 / cint(doc.no_of_columns_all_books or 4))
	context.display_all_books_as = doc.display_all_books_as or 'Grid'
	context.filter_position = doc.filter_position
	context.parents = [
		{ "name": frappe._("Home"), "route": "/" }
	]
	if frappe.form_dict:
		search = frappe.form_dict.q
		search_category = frappe.form_dict.category
		field_filters = frappe.parse_json(frappe.form_dict.field_filters)
		attribute_filters = frappe.parse_json(frappe.form_dict.attribute_filters)
	else:
		search = field_filters = attribute_filters = None
		search_category = 'General'

	product_settings = get_product_settings()
	context.field_filters = get_field_filter_data() \
		if product_settings.enable_field_filters else []

	context.attribute_filters = get_attribute_filter_data() \
		if product_settings.enable_attribute_filters else []

	context.product_settings = product_settings
	context.page_length = product_settings.products_per_page

	context.items = get_products_for_website(field_filters, attribute_filters, search, search_category)
	context.itemscount = (get_products_for_website_count(field_filters, attribute_filters, search, search_category)) or []





	context.no_cache = 1
