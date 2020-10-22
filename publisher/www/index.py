# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, fmt_money, flt, nowdate, getdate, global_date_format, strip_html_tags
from erpnext.setup.doctype.item_group.item_group import get_product_list_for_group
from erpnext.setup.doctype.item_group.item_group import get_group_item_count
#from frappe.website.doctype.blog_post.blog_post import get_blog_list
from frappe.website.utils import (find_first_image, get_html_content_based_on_type)

no_cache = 1
no_sitemap = 1

def get_context(context):

	homepage = frappe.get_doc('Website Homepage Settings')
	context.title = homepage.title

	if homepage.slideshow:
		context.slideshow = homepage.slideshow
		context.update(get_slideshow_details(homepage.slideshow))

	if homepage.section_item:
		context["homepage_section_item"] = get_section_item_details()
	if homepage.author_section_title and homepage.author:
		context["author_section_title"] = homepage.author_section_title
		context["author_section_description"] = homepage.author_section_description
		context["author"] = homepage.author
		context["author_display_after_section_item_row_number"] = homepage.display_after_section_item_row_number
		context.author_doc = frappe.get_doc("Author", homepage.author)
		#context.author_doc.description = (context.author_doc.description[:497] + '...') if len(context.author_doc.description) > 500 else context.author_doc.description
		context["author_books"] = frappe.db.get_all('Item',filters={'author': homepage.author,'show_in_website': 1},fields=['item_name', 'website_image','image','route'],order_by='publication_date DESC', start=0, page_length=10)

	if homepage.allow_blog_section:
		context["allow_blog_section"] = homepage.allow_blog_section
		context["blog_section_title"] = homepage.blog_section_title
		context["blog_section_description"] = homepage.blog_section_description
		context["display_blog_after_section_item_row_number"] = homepage.display_blog_after_section_item_row_number
		context["display_blog_as"] = homepage.display_blog_as
		if homepage.number_of_columns_of_blog_items:
			if homepage.display_blog_as == 'Grid':
				context["number_of_columns_of_blog_items"] = cint(12 / cint(homepage.number_of_columns_of_blog_items or 3))
			else:
				context["number_of_columns_of_blog_items"] = homepage.number_of_columns_of_blog_items
		context["max_number_to_display_of_blog"] = homepage.max_number_to_display_of_blog or 10
		#context["blog_items"] = get_blog_list('Blog Post', None, None, 0, 10, 'published_on')
		blog_items = frappe.db.get_all('Blog Post',filters={'published': 1},fields=['title','published_on','blog_category','blogger', 'route','blog_intro','content','content_type','content_html','content_md'],order_by='published_on DESC', start=0, page_length=homepage.max_number_to_display_of_blog or 10)
		if blog_items :
			for post in blog_items:
				post.blog_category = frappe.db.get_value('Blog Category', post.blog_category, 'title')
				post.blogger = frappe.db.get_value('Blogger', post.blogger, 'full_name')
				post.content = get_html_content_based_on_type(post, 'content', post.content_type)
				post.cover_image = find_first_image(post.content)
				post.published = global_date_format(post.published_on)
				post.content = strip_html_tags(post.content)
			context["blog_items"] = blog_items
		else:
			context["blog_items"] = []

	return context

def get_slideshow_details(slideshow):

	slideshow = frappe.get_doc("Website Slideshow", slideshow)
	if not slideshow:
		return {}

	return {
		"slides": slideshow.get({"doctype":"Website Slideshow Item"}),
		"slideshow_header": slideshow.header or ""
	}


def get_section_item_details():
	all_item_sections = frappe.db.get_all('Website Homepage Section Item',fields=['section_type', 'section_theme', 'website_section', 'item_group_name', 'display_item_group_as', 'number_of_columns_item', 'max_number_to_display_item_group','idx'],order_by='idx asc')

	adjusted_data = []

	for section in all_item_sections:
		#section['section_theme_details'] = frappe.db.get_list('Website Section Theme',filters={'name': section.section_theme},fields=['class_name', 'custom_background', 'background_image', 'background_video', 'removing_top_border'])
		section['section_theme_details'] = get_section_theme_details(section.section_theme)
		if section.section_type == "Item Group" and section.item_group_name:
			section['item_group_route'] = frappe.db.get_value('Item Group', section.item_group_name, 'route')
			if section.max_number_to_display_item_group == 0:
				section.max_number_to_display_item_group = 10
			if section.display_item_group_as == 'Grid':
				section['number_of_columns_item'] = cint(12 / cint(section.number_of_columns_item or 3))
			section['product_items'] = get_product_list_for_group(section.item_group_name,0,section.max_number_to_display_item_group)
		if section.section_type == "Website Section" and section.website_section:
			section['website_section_details'] = get_website_section_details(section.website_section)
		adjusted_data.append(section)

	return adjusted_data


def get_section_theme_details(section_theme):
	section_theme_details = frappe.db.get_value('Website Section Theme', section_theme, ['class_name', 'custom_background', 'background_image', 'background_video', 'removing_top_border', 'removing_margin_top_and_bottom', 'with_divider', 'center_aligned'], as_dict=1)

	return section_theme_details

def get_website_section_details(website_section):
	website_section_details = frappe.db.get_value('Website Section', website_section, ['name','section_based_on', 'show_section_title', 'no_of_columns', '12/no_of_columns as column_value', 'section_html'], as_dict=1)
	if website_section_details.column_value:
		website_section_details.column_value = cint(12 / cint(website_section_details.no_of_columns or 3))
	if website_section_details.section_based_on == "Cards":
		adjusted_data = []
		website_section_details['section_cards'] = frappe.db.get_all('Website Section Card', filters={'parent': website_section_details.name}, fields=['title', 'subtitle', 'show_card_title', 'text_center_aligned', 'image_type', 'icon','image', 'content', 'route'],order_by='idx asc')
		adjusted_data.append(website_section_details)
	else:
		adjusted_data = website_section_details

	#website_section_details = frappe.db.get_all('Website Section', filters={'name': website_section}, fields=['section_based_on', 'show_section_title', 'no_of_columns', 'section_cards', 'section_html'])

	return adjusted_data
