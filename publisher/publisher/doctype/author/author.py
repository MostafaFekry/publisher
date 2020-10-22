# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint
from frappe.website.website_generator import WebsiteGenerator
from publisher.publisher.product_configurator.utils import (get_products_for_website)

class Author(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/author.html",
		condition_field = "show_in_website",
		page_title_field = "author_name",
		no_cache = 1
	)
	def validate(self):
		if not self.route:
			self.route = 'authors/' +self.scrub(self.author_name)
		super(Author, self).validate()

	def get_context(self, context):
		context.main_section = self.description or self.author_summary
		context.title = self.author_name
		context.author_social_media = self.author_social_media
		doc = frappe.get_doc("Website Authors Settings", "Website Authors Settings")
		context.author_publication_title = doc.author_publication_title
		context.display_all_books_as = doc.display_item_as
		context.all_books_column_value = cint(12 / cint(doc.no_of_items_columns or 4))
		context.bookroute = self.name
		filterby = {"author":[self.name]}
		context.update({
			"parents": [{"name": frappe._("Home"), "route":"/"},{"name": frappe._("Authors"), "route":"/authors"}],
			"author_image": self.image,
			"items":get_products_for_website(field_filters=frappe.parse_json(filterby), attribute_filters=None, search=None)
		})

		return context

@frappe.whitelist(allow_guest=True)
def get_author_for_list_in_html(start, limit, search,sort_by):
	#set order_by value
	if sort_by == 'namedesc':
		order_by = "author_name DESC"
	else:
		order_by = "author_name asc"

	search_filters = None
	if search_filters:
		search_filters = [
			dict(author_name = ('like', '%{}%'.format(search))),
			dict(description = ('like', '%{}%'.format(search)))
		]
	data = frappe.db.get_all('Author',
		fields = ['author_name', 'route', 'description', 'image'],
		filters = dict(
			show_in_website = 1,
		),
		or_filters = search_filters,
		order_by = order_by or 'author_name asc',
		start = start,
		limit = limit
	)
	items_count = frappe.db.count('Author',{'show_in_website': 1})
	return items_count , data
