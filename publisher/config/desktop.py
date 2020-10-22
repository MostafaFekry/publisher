# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Publisher",
			"category": "Places",
			"label": _("Publisher"),
			"color": "#8e44ad",
			"icon": "octicon octicon-book",
			"type": "module",
			"description": "Publishers."
		},
		{
			"module_name": "Publisher Website",
			"category": "Places",
			"label": _("Publisher Website"),
			"_label": _("Publisher Website"),
			"color": "#16a085",
			"icon": "octicon octicon-globe",
			"type": "module",
			"description": "Webpages, webforms, blogs and website theme."
		},
	]
