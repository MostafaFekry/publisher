from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Publisher Cycle"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Argument",
					"description": _("Content Argument."),
                    "onboard": 1,
				},
				{
					"type": "doctype",
					"name": "Author",
					"description": _("Author Details."),
					"onboard": 1,

				},
 			]
		},
   		{
			"label": _("Setup"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"label": _("Author Group"),
					"name": "Author Group",
					"icon": "fa fa-sitemap",
					"description": _("Manage Author Group Tree."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"label": _("ISBN Form"),
					"name": "ISBN Form",
					"icon": "fa fa-sitemap",
					"description": _("Manage ISBN Form."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"label": _("Binding"),
					"name": "Binding",
					"icon": "fa fa-sitemap",
					"description": _("Manage Publication Binding Type."),
				},
				{
					"type": "doctype",
					"label": _("Publication Language"),
					"name": "Publication Language",
					"icon": "fa fa-sitemap",
					"description": _("Manage Publication Language."),
				},
				{
					"type": "doctype",
					"label": _("Publication Subject"),
					"name": "Publication Subject",
					"icon": "fa fa-sitemap",
					"description": _("Manage publication subject list."),
				},
				{
					"type": "doctype",
					"label": _("Illustrator"),
					"name": "Illustrator",
					"icon": "fa fa-sitemap",
					"description": _("Manage list of Illustrator."),
				},
				{
					"type": "doctype",
					"label": _("Publication Series"),
					"name": "Publication Series",
					"icon": "fa fa-sitemap",
					"description": _("List of Publication Series."),
				},
				{
					"type": "doctype",
					"label": _("Publication Age Range"),
					"name": "Publication Age Range",
					"icon": "fa fa-sitemap",
					"description": _("Manage Publication Age Range Type."),
				},
				{
					"type": "doctype",
					"label": _("Publication Grade Range"),
					"name": "Publication Grade Range",
					"icon": "fa fa-sitemap",
					"description": _("List of Publication Grade Range."),
				},
				{
					"type": "doctype",
					"label": _("Publication Award"),
					"name": "Publication Award",
					"icon": "fa fa-sitemap",
					"description": _("List of Publication Awards."),
				},
			]
		},
		{
			"label": _("Documents"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"label": _("Contracting"),
					"name": "Contracting",
					"icon": "fa fa-sitemap",
					"description": _("Manage Contracting."),
					"onboard": 1,
				},
				{
					"type": "doctype",
					"label": _("Evaluation"),
					"name": "Evaluation",
					"icon": "fa fa-sitemap",
					"description": _("Manage Evaluation."),
					"onboard": 1,
				},
			]

		},
	]
