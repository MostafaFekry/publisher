# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, fmt_money, flt, nowdate, getdate

no_cache = 1
no_sitemap = 1

def get_context(context):
	context.doc = frappe.get_doc("Website About Us Settings", "Website About Us Settings")
	context.title = context.doc.title or "About us"
	context.column_value = cint(12 / cint(context.doc.no_of_columns or 3))
	context.column_value_about_item = cint(12 / cint(context.doc.no_of_columns_about_item or 2))
	context.column_value_member_item = cint(12 / cint(context.doc.no_of_columns_member_item or 4))

	context.parents = [
		{ "name": frappe._("Home"), "route": "/" }
	]

	return context
