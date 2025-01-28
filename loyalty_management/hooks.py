app_name = "loyalty_management"
app_title = "Loyalty Management"
app_publisher = "Yemen Frappe"
app_description = "Loyalty Management"
app_email = "exam@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/loyalty_management/css/loyalty_management.css"
# app_include_js = "/assets/loyalty_management/js/loyalty_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/loyalty_management/css/loyalty_management.css"
# web_include_js = "/assets/loyalty_management/js/loyalty_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "loyalty_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    
    "Loyalty Program": "public/js/loyalty_program.js",
    "Item": "public/js/item.js",
    # "Customer": "public/js/customer_dashboard.js",

    
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "loyalty_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "loyalty_management.utils.jinja_methods",
# 	"filters": "loyalty_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "loyalty_management.install.before_install"
after_install = "loyalty_management.loyalty_management.overrides.cache_manager.extend_doctype_mapping"

# after_install = "loyalty_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "loyalty_management.uninstall.before_uninstall"
# after_uninstall = "loyalty_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "loyalty_management.utils.before_app_install"
# after_app_install = "loyalty_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "loyalty_management.utils.before_app_uninstall"
# after_app_uninstall = "loyalty_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "loyalty_management.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	
    "Sales Invoice": "loyalty_management.loyalty_management.overrides.sales_invoice.CustomSalesInvoice",
    "Loyalty Program": "loyalty_management.loyalty_management.overrides.loyalty_program.CustomLoyaltyProgram",
    "Loyalty Point Entry": "loyalty_management.loyalty_management.overrides.loyalty_point_entry.CustomLoyaltyPointEntry",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"*": {
		# "on_update": "method",
		# "on_cancel": "method",
		# "on_trash": "method",
        "on_change": [
			"loyalty_management.loyalty_management.overrides.loyalty_program.process_loyalty_points",
			
		],
	}
    
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"loyalty_management.tasks.all"
# 	],
# 	"daily": [
# 		"loyalty_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"loyalty_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"loyalty_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"loyalty_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "loyalty_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# "frappe.desk.doctype.event.event.get_events": "loyalty_management.event.get_events"
    "erpnext.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_program_details_with_points": "loyalty_management.loyalty_management.overrides.loyalty_program.get_loyalty_program_details_with_points",

}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "loyalty_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["loyalty_management.utils.before_request"]
# after_request = ["loyalty_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["loyalty_management.utils.before_job"]
# after_job = ["loyalty_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"loyalty_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

