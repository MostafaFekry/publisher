# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WebsiteBlogSettings(Document):
	def on_update(self):
		from frappe.website.render import clear_cache
		clear_cache("blog")
		clear_cache("writers")
