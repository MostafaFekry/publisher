# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.render import clear_cache

class WebsiteBlogCategory(WebsiteGenerator):
	def autoname(self):
		# to override autoname of WebsiteGenerator
		self.name = self.category_name

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = 'blog/general/' + self.scrub(self.name)
		super(WebsiteBlogCategory, self).validate()
