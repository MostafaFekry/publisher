from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Web Site"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Web Page",
					"description": _("Content web page."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Web Form",
					"description": _("User editable form on Website."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Website Sidebar",
				},
				{
					"type": "doctype",
					"name": "Website Slideshow",
					"description": _("Embed image slideshows in website pages."),
				},
				{
					"type": "doctype",
					"name": "Website Route Meta",
					"description": _("Add meta tags to your web pages"),
				},
			]
		},
		{
			"label": _("Pages"),
			"items": [
				{
					"type": "doctype",
					"name": "Website Homepage Settings",
					"description": _("Settings for Home Page."),
				},
				{
					"type": "doctype",
					"name": "Website Authors Settings",
					"description": _("Settings for Authors Page."),
				},
				{
					"type": "doctype",
					"name": "Website About Us Settings",
					"description": _("Settings for About Us Page."),
				},
				{
					"type": "doctype",
					"name": "Website Contact Us Settings",
					"description": _("Settings for Contact Us Page."),
				},
			]
		},
		{
			"label": _("Blog"),
			"items": [
				{
					"type": "doctype",
					"name": "Blog Post",
					"description": _("Single Post (article)."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Blogger",
					"description": _("A user who posts blogs."),
				},
				{
					"type": "doctype",
					"name": "Blog Category",
					"description": _("Categorize blog posts."),
				},
				{
					"type": "doctype",
					"name": "Blog Settings",
					"description": _("Settings for Blog Page."),
				},
			]
		},
		{
			"label": _("Setup"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Website Settings",
					"description": _("Setup of top navigation bar, footer and logo."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Publisher Website Settings",
					"description": _("Setup of top navigation bar, footer and logo."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Website Section",
					"description": _("List of Website Section for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Theme Settings",
					"description": _("List of themes for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Script",
					"description": _("Javascript to append to the head section of the page."),
				},
				{
					"type": "doctype",
					"name": "Website Social Media",
					"description": _("List of Social Media for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Section Theme",
					"description": _("List of Section Theme for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Background Pattern",
					"description": _("List of Background Pattern for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Header Design",
					"description": _("List of Header Design for Website."),
				},
				{
					"type": "doctype",
					"name": "Website Page Header Design",
					"description": _("List of Page Header Design for Website."),
				},
			]
		},
		{
			"label": _("Portal"),
			"items": [
				{
					"type": "doctype",
					"name": "Portal Settings",
					"label": _("Portal Settings"),
					"onboard": 1,
				}
			]
		},
		{
			"label": _("Knowledge Base"),
			"items": [
				{
					"type": "doctype",
					"name": "Help Category",
				},
				{
					"type": "doctype",
					"name": "Help Article",
				},
			]
		},

	]
