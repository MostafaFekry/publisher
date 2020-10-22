# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "publisher"
app_title = "Publisher"
app_publisher = "Alzad"
app_description = "An app for handling publishing process"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "a.moustafa@alzad.ae"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/publisher/css/publisher.css"
# app_include_js = "/assets/publisher/js/publisher.js"

# include js, css files in header of web template
# web_include_css = "/assets/publisher/css/publisher.css"
# web_include_js = "/assets/publisher/js/publisher.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "publisher.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# website
update_website_context = "publisher.utils.update_website_context"


#website_route_rules = [
#	{"from_route": "/blog/general/<category>", "to_route": "Blog"},
#	{"from_route": "/blog/general", "to_route": "Blog"},
#]

#before_install = "publisher.publisher_install.install.before_install"
after_install = "publisher.publisher_install.install.after_install"


# fixtures
fixtures = [{"dt": "Author"}]

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "publisher.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"publisher.tasks.all"
# 	],
# 	"daily": [
# 		"publisher.tasks.daily"
# 	],
# 	"hourly": [
# 		"publisher.tasks.hourly"
# 	],
# 	"weekly": [
# 		"publisher.tasks.weekly"
# 	]
# 	"monthly": [
# 		"publisher.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "publisher.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "publisher.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "publisher.task.get_dashboard_data"
# }
