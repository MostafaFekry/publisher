# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, fmt_money, flt, nowdate, getdate
from publisher.publisher.doctype.author.author import get_author_for_list_in_html

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.doc = frappe.get_doc("Website Authors Settings", "Website Authors Settings")
	context.page_length = cint(context.doc.authors_per_page) or 10
	context.column_value = cint(12 / cint(context.doc.no_of_columns or 3))

	start = int(frappe.form_dict.start or 0)
	if start < 0:
		start = 0
	author_count, author_items = get_author_for_list_in_html(start=start, limit=context.page_length + 1, search=frappe.form_dict.get("search") or None, sort_by=frappe.form_dict.sort or None)
	context.items = author_items
	context.author_items_count = author_count
	context.update({
		"parents": [{ "name": frappe._("Home"), "route": "/" }],
		"title": context.doc.title or "Authors"
	})

	return context
