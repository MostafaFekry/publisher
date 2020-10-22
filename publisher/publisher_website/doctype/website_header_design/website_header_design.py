# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class WebsiteHeaderDesign(Document):
	def set_as_default(self):
		publisher_website_settings = frappe.get_doc('Publisher Website Settings')
		publisher_website_settings.website_header_design = self.name
		publisher_website_settings.ignore_validate = True
		publisher_website_settings.save()


def add_website_header(context):
	context.headerdesign = frappe._dict()
	website_headerdesign = get_active_header()
	context.headerdesign = website_headerdesign and website_headerdesign.as_dict() or frappe._dict()

def get_active_header():
	website_header_design = frappe.db.get_value("Publisher Website Settings", "Publisher Website Settings", "website_header_design")
	if website_header_design:
		try:
			return frappe.get_doc("Website Header Design", website_header_design)
		except frappe.DoesNotExistError:
			pass
