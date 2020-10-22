# -*- coding: utf-8 -*-
# Copyright (c) 2020, Alzad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from publisher.publisher_install.install import (make_website_settings, update_item_group_items, update_website_section_items,update_website_homepage_settings,update_website_authors_settings,update_website_about_us_settings,update_website_contact_us_settings)
from publisher.publisher_install.install_add_examples import add_examples

class PublisherWebsiteSettings(Document):
	def update_publisher_app(self):
		default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
		default_language = frappe.db.get_single_value('System Settings', 'language')
		confirm = False
		ignor_language = True
		make_website_settings(default_company)
		update_item_group_items()
		update_website_section_items(confirm)
		update_website_homepage_settings(confirm,default_language=None,ignor_language=True)
		update_website_authors_settings(confirm)
		update_website_about_us_settings(confirm)
		update_website_contact_us_settings(confirm)
		self.publication_item_group = _("Publication")
		self.all_data_added_to_publisher = 1
		self.save()

	def add_examples_data(self):
		add_examples()
		self.allow_payment_image_in_footer = 1
		self.example_data_updated = 1
		self.save()
