# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from frappe.model.document import Document

class WebsiteBlogger(Document):
	def validate(self):
		if self.user and not frappe.db.exists("User", self.user):
			# for data import
			frappe.get_doc({
				"doctype":"User",
				"email": self.user,
				"first_name": self.user.split("@")[0]
			}).insert()

	def on_update(self):
		"if user is set, then update all older blogs"

		from publisher.publisher_website.doctype.blog.blog import clear_blog_cache
		clear_blog_cache()

		if self.user:
			for blog in frappe.db.sql_list("""select name from `tabBlog` where owner=%s
				and ifnull(blogger,'')=''""", self.user):
				b = frappe.get_doc("Blog", blog)
				b.blogger = self.name
				b.save()

			frappe.permissions.add_user_permission("Blogger", self.name, self.user)
