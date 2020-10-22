# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, msgprint, _
from frappe.utils import cint ,get_request_site_address, encode

from frappe.model.document import Document
from erpnext.setup.doctype.item_group.item_group import get_group_item_count,get_product_list_for_group
from publisher.publisher_website.doctype.website_theme_settings.website_theme_settings import add_website_theme
from publisher.publisher_website.doctype.website_header_design.website_header_design import add_website_header
from publisher.publisher_website.doctype.website_page_header_design.website_page_header_design import add_website_page_header


def update_website_context(context):
	website_languages_request = frappe.form_dict._lang
	if website_languages_request:
		context["website_languages_request"] = website_languages_request
	else:
		default_website_languages_item = get_default_website_languages()
		if default_website_languages_item:
			for item in default_website_languages_item:
				if item.get("language"):
					context["mytestnew"] = item.get("language")
					context["website_languages_request"] = item.get("language")
					website_languages_request = item.get("language")
				else:
					website_languages_request =  frappe.db.get_single_value('System Settings', 'language')
					context["website_languages_request"] = website_languages_request
		else:
			website_languages_request =  frappe.db.get_single_value('System Settings', 'language')
			context["website_languages_request"] = website_languages_request

	context["website_languages_items"] = get_website_languages_items()
	if context["website_languages_items"]:
		context.update(get_website_languages_details(website_languages_request))

	website_settings = frappe.get_doc('Publisher Website Settings')
	context["enable_multilanguage_support"] = website_settings.enable_multilanguage_support
	context["display_language_picker_in_top_bar"] = website_settings.display_language_picker_in_top_bar
	#context["link_number_in_footer_row"] = website_settings.link_number_in_footer_row
	#context["footer_contact_number"] = website_settings.footer_contact_number
	#context["footer_contact_email"] = website_settings.footer_contact_email

	context["website_social_media_item"] = website_settings.website_social_media_item
	context["display_social_links_on_header_top_bar"] = website_settings.display_social_links_on_header_top_bar or 0
	context["display_social_links_on_footer"] = website_settings.display_social_links_on_footer

	context["website_top_bar_item_group"] = website_settings.publication_item_group
	context["website_top_bar_item_group_design"] = website_settings.sub_menu_design

	# Mostafa return item groups sidebar items
	context["sidebarshow_item_group"] = sidebarshow_item_group()

	context["website_all_books_page_title"] = website_settings.all_books_page_title or "All Books"
	context["website_display_sidebar_category_in_publication_categories"] = website_settings.display_sidebar_category_in_publication_categories
	context["website_display_category_items_as"] = website_settings.display_category_items_as
	context["website_no_of_columns_category"] = cint(12 / cint(website_settings.no_of_columns_category or 3))
	context["website_display_sidebar_category_in_publication_items"] = website_settings.display_sidebar_category_in_publication_items
	context["website_display_publication_items_as"] = website_settings.display_publication_items_as
	context["website_no_of_columns_publication_items"] = cint(12 / cint(website_settings.no_of_columns_publication_items or 3))
	context["website_no_img_available"] = "/assets/publisher/img/noimageavailable.gif"
	context["login_required"] = website_settings.login_required
	context["allow_rating"] = website_settings.allow_rating
	context["max_comments_show"] = website_settings.max_comments_show
	context["publication_item_enable_comments"] = website_settings.publication_item_enable_comments
	context["max_post_allowed"] = website_settings.max_post_allowed
	context["footer_copyright_year"] = website_settings.copyright_year
	context["footer_allow_payment_image_in_footer"] = website_settings.allow_payment_image_in_footer

	# return custom website theme settings
	add_website_theme(context)

	# return website header design settings
	add_website_header(context)

	# return website Page header design settings
	add_website_page_header(context)

	# Mostafa return related items for item
	context["related_items_details"] = related_items_details()


def get_default_website_languages():
	all_language_items = frappe.db.sql("""\
		select language from `tabWebsite Languages`
		where parent='Publisher Website Settings'
		order by idx asc LIMIT 1""", as_dict=1)
	if all_language_items:
		website_languages_items = [d for d in all_language_items]
	else:
		website_languages_items = []
	return website_languages_items

def get_website_languages_items():
	all_language_items = frappe.db.sql("""\
		select * from `tabWebsite Languages`
		where parent='Publisher Website Settings'
		order by idx asc""", as_dict=1)
	if all_language_items:
		website_languages_items = [d for d in all_language_items]
	else:
		website_languages_items = []
	return website_languages_items


def get_website_languages_details(website_languages_request="en"):
	website_languages_details = frappe.get_doc("Website Languages", website_languages_request)
	if not website_languages_details:
		return {}

	return {
		"website_languages_name": website_languages_details.language_name,
		"website_languages_flag": website_languages_details.language_flag,
		"website_languages_flag_image": website_languages_details.language_flag_image,
		"main_page_title": website_languages_details.main_page_title,
		"top_header_message": website_languages_details.top_header_message,
		"allow_top_bar_notice": website_languages_details.allow_top_bar_notice,
		"top_bar_notice": website_languages_details.top_bar_notice,
		"allow_display_contact_on_footer": website_languages_details.allow_display_contact_on_footer,
		"footer_company_information_title": website_languages_details.footer_company_information_title,
		"footer_address_title": website_languages_details.footer_address_title,
		"footer_address_details": website_languages_details.footer_address_details,
		"footer_tel_title": website_languages_details.footer_tel_title,
		"footer_tel_details": website_languages_details.footer_tel_details,
		"footer_email_title": website_languages_details.footer_email_title,
		"footer_email_details": website_languages_details.footer_email_details,
		"footer_social_media_title": website_languages_details.footer_social_media_title,
		"footer_newsletter_title": website_languages_details.footer_newsletter_title,
		"footer_newsletter_details": website_languages_details.footer_newsletter_details,
		"footer_newsletter_input_title": website_languages_details.footer_newsletter_input_title,
		"footer_newsletter_send_button_title": website_languages_details.footer_newsletter_send_button_title,
		"website_languages_copyright": website_languages_details.copyright
	}

def sidebarshow_item_group():
	# Mostafa return item groups sidebar items
	all_item_group = frappe.db.sql("""\
		select IG.item_group_name,IG.show_in_website,IG.route,IG.is_group,IG.parent_item_group,IG.lft,IG.rgt from `tabItem Group` IG
		where IG.show_in_website=1
		order by IG.lft asc""", as_dict=1)

	item_group = all_item_group[:]

	# attach child items to top bar
	for d in all_item_group:
		for t in item_group:
			if t['item_group_name']==d['parent_item_group']:
				if not 'child_items' in t:
					t['child_items'] = []
				t['child_items'].append(d)
				break

	data = [d for d in all_item_group]

	sidebarshow_item_group = adjust_group_item_count_items(data)

	return sidebarshow_item_group

def adjust_group_item_count_items(data):
	adjusted_data = []

	for item in data:
		if not item.get('is_group'):
			item['item_item_group_count'] = get_group_item_count(item.get('item_group_name'))
		else:
			item['item_item_group_count'] = 0
		adjusted_data.append(item)

	return adjusted_data

def related_items_details():
	if hasattr(frappe.local, 'request'):
		# for <body data-path=""> (remove leading slash)
		# path could be overriden in render.resolve_from_map
		pageroute = frappe.local.request.path.strip('/ ')

	if pageroute:
		item_group = frappe.db.get_value('Item', {'route': pageroute}, ['item_group'])
		if item_group:
			related_items = get_product_list_for_group(item_group) or ""
		else:
			related_items = ""
	else:
		related_items = ""
	return related_items
