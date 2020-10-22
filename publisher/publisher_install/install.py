# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe, os, json ,click

from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.utils import cstr, getdate, update_progress_bar
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def before_install():
	frappe.reload_doc("core", "doctype", "docfield")
	frappe.reload_doc("core", "doctype", "docperm")
	frappe.reload_doc("core", "doctype", "doctype")

def after_install():
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	default_language = frappe.db.get_single_value('System Settings', 'language')
	default_warehouse = frappe.db.get_single_value('Stock Settings', 'default_warehouse')
	confirm = False
	install_workflow_docs()
	create_item_custom_field()
	create_other_custom_field()

	update_social_media_items()
	update_website_background_pattern_items()
	update_website_section_theme_items()
	update_website_theme_settings_standard()
	update_website_header_design_items()
	update_website_page_header_design_items()
	make_products_settings()
	make_website_settings(default_company)

	if default_language == 'en':
		update_item_group_items()


	if default_language == 'en':
		confirm = click.confirm("Allow to update site with demo examples. Are you sure you want to continue?")
		print("Your select {0}...".format(confirm))

	if confirm:
		update_author_items()
		update_website_slideshow()
		update_item_group_extra_items()
		update_binding_items()
		update_publication_language_items()
		update_publication_subject_items()
		update_illustrator_items()
		update_publication_series_items()
		update_publication_age_range_items()
		update_publication_grade_range_items()
		update_publication_award_items()
		update_item_items(default_warehouse)

	if default_language == 'en':
		update_website_section_items(confirm)

	update_website_homepage_settings(confirm,default_language)
	update_website_authors_settings(confirm)
	update_website_about_us_settings(confirm)
	update_website_contact_us_settings(confirm)
	update_shopping_cart_settings()



	update_publisher_website_settings(confirm,default_company,default_language)

	#create_slideshow_custom_field()
	#create_topbar_websitesetting_custom_field()
	if not default_language == 'en':
		print("--- You able to update publisher data and examples from Publisher Website Setting Doctype---")
	print("\n---------------\nPublisher successfully installed :)")
	frappe.db.commit()

def install_workflow_docs():
	# Workflow / Workflow State /Workflow Action Master
	install_docs = [
		{'doctype':'Workflow State', 'workflow_state_name':'Applied', 'style':'Info'},
		{'doctype':'Workflow State', 'workflow_state_name':'Approved by', 'style':'Info'},
		{'doctype':'Workflow State', 'workflow_state_name':'Approved by Publisher', 'style':'Info'},
		{'doctype':'Workflow State', 'workflow_state_name':'Cancelled', 'style':'Danger'},
		{'doctype':'Workflow State', 'workflow_state_name':'Contracting', 'style':'Primary'},
		{'doctype':'Workflow State', 'workflow_state_name':'Proofreading', 'style':'Primary'},
		{'doctype':'Workflow State', 'workflow_state_name':'Design', 'style':'Warning'},
		{'doctype':'Workflow State', 'workflow_state_name':'ISBN', 'style':'Success'},
		{'doctype': "Workflow Action Master", "workflow_action_name": "ISBN"},
		{'doctype': "Workflow Action Master", "workflow_action_name": "Design"},
		{'doctype': "Workflow Action Master", "workflow_action_name": "Proofreading"},
		{'doctype': "Workflow Action Master", "workflow_action_name": "Contracting"},
		{'doctype':'Workflow', 'workflow_name':'Argument Approval ', 'document_type':'Argument', 'is_active':1, 'override_status':0, "send_email_alert": 0, 'workflow_state_field':'workflow_state',
			'states': [{'state': 'Applied', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Applied', 'is_optional_state':0},
			{'state': 'Approved', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Approved', 'is_optional_state':0},
			{'state': 'Rejected', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Rejected', 'is_optional_state':0},
			{'state': 'Approved', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Contracting', 'is_optional_state':0},
			{'state': 'Contracting', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Contracting', 'is_optional_state':0},
			{'state': 'Contracting', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Proofreading', 'is_optional_state':0},
			{'state': 'Proofreading', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Proofreading', 'is_optional_state':0},
			{'state': 'Design', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Design', 'is_optional_state':0},
			{'state': 'ISBN', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'ISBN Issued', 'is_optional_state':0},
			{'state': 'Cancelled', 'allow_edit':'System Manager','doc_status':0, 'update_field':'workflow_state', 'update_value':'Closed', 'is_optional_state':0}],
			'transitions': [{'state': 'Applied', 'action':'Approve','next_state':'Approved', 'allowed':'System Manager', 'allow_self_approval':1},
			{'state': 'Applied', 'action':'Reject','next_state':'Rejected', 'allowed':'System Manager', 'allow_self_approval':1},
			{'state': 'Approved', 'action':'Contracting','next_state':'Contracting', 'allowed':'System Manager', 'allow_self_approval':1},
			{'state': 'Contracting', 'action':'Proofreading','next_state':'Proofreading', 'allowed':'System Manager', 'allow_self_approval':1},
			{'state': 'Proofreading', 'action':'Design','next_state':'Design', 'allowed':'System Manager', 'allow_self_approval':1},
			{'state': 'Design', 'action':'ISBN','next_state':'ISBN', 'allowed':'System Manager', 'allow_self_approval':1}]
		}]

	for d in install_docs:
		try:
			frappe.get_doc(d).insert()
		except frappe.NameError:
			pass

def create_item_custom_field():
	records = [
		{'label':_('Publication Details'), 'fieldname':'publication_details', 'fieldtype':'Section Break','insert_after':'image'},
		{'label':_('Author'), 'fieldname':'author', 'fieldtype':'Link', 'options':'Author','insert_after':'publication_details'},
		{'label':_('ISBN'), 'fieldname':'isbn', 'fieldtype':'Link', 'options':'ISBN Form','insert_after':'author'},
		{'label':_('Binding'), 'fieldname':'binding', 'fieldtype':'Link', 'options':'Binding','insert_after':'isbn'},
		{'label':_('Language'), 'fieldname':'language', 'fieldtype':'Link', 'options':'Publication Language','insert_after':'binding'},
		{'label':_('Age Range'), 'fieldname':'age_range', 'fieldtype':'Link', 'options':'Publication Age Range','insert_after':'language'},
		{'label':_('Grade Range'), 'fieldname':'grade_range', 'fieldtype':'Link', 'options':'Publication Grade Range','insert_after':'age_range'},
		{'label':_('Series'), 'fieldname':'series', 'fieldtype':'Check','insert_after':'grade_range'},
		{'label':_('Series Name'), 'fieldname':'series_name', 'fieldtype':'Link', 'options':'Publication Series','insert_after':'series', 'depends_on':'series'},
		{'label':_('Series Number'), 'fieldname':'series_number', 'fieldtype':'Int','insert_after':'series_name', 'depends_on':'series'},
		{'label':_('Illustration'), 'fieldname':'illustration', 'fieldtype':'Check','insert_after':'series_number'},
		{'label':_('Illustrator'), 'fieldname':'illustrator', 'fieldtype':'Link', 'options':'Illustrator', 'depends_on':'illustration','insert_after':'illustration'},
		{'fieldname':'col_custom_001', 'fieldtype':'Column Break','insert_after':'illustrator'},
		{'label':_('Publication Date'),'fieldname':'publication_date', 'fieldtype':'Date','insert_after':'col_custom_001'},
		{'label':_('Pages'),'fieldname':'pages', 'fieldtype':'Int','insert_after':'publication_date'},
		{'label':_('Number of Units'),'fieldname':'number_of_units', 'fieldtype':'Int','insert_after':'pages'},
		{'label':_('Width (INCH)'),'fieldname':'publication_width_in', 'fieldtype':'Float','insert_after':'number_of_units', 'precision':2},
		{'label':_('Height (INCH)'),'fieldname':'publication_height_in', 'fieldtype':'Float','insert_after':'publication_width_in', 'precision':2},
		{'label':_('Thickness'),'fieldname':'publication_thickness', 'fieldtype':'Float','insert_after':'publication_height_in', 'precision':2},
		{'label':_('Subject'),'fieldname':'subject', 'fieldtype':'Table MultiSelect','options':'Item Publication Subject','insert_after':'publication_thickness'},
		{'label':_('Awards'),'fieldname':'awards', 'fieldtype':'Table MultiSelect','options':'Item Publication Award','insert_after':'subject'}]

	for i, r in enumerate(records):
		update_progress_bar("Updating Publication Item Fields for Item", i, len(records))
		create_custom_field('Item', r)


def create_other_custom_field():
	print("\nUpdate other custom fields")
	# Website Slideshow Item
	records = [{'label':_('Slider Description'), 'fieldname':'slider_description', 'fieldtype':'Section Break','insert_after':'image'},
		{'fieldname':'column_break_4', 'fieldtype':'Column Break','insert_after':'description'},
		{'label':_('Set Position'), 'fieldname':'set_position', 'fieldtype':'Select', 'options':'Left\nRight\nCenter\nDown','insert_after':'column_break_4', 'default':'Left', 'in_list_view':1,'description':'Position of slider description.'},
		{'label':_('Link Title'), 'fieldname':'link_title', 'fieldtype':'Data', 'translatable':1,'insert_after':'set_position'},
		{'label':_('Link Path'), 'fieldname':'link_path', 'fieldtype':'Data','insert_after':'link_title'},
		{'label':_('Link Target'), 'fieldname':'link_target', 'fieldtype':'Select', 'options':'\ntarget=\"_blank\"', 'insert_after':'link_path'}]
	for r in records:
		create_custom_field('Website Slideshow Item', r)

	# Comment
	records = [{'label':_('Publication Rating'), 'fieldname':'publication_rating', 'fieldtype':'Rating','insert_after':'comment_by'}]
	for r in records:
		create_custom_field('Comment', r)
	# Top Bar Item
	records = [{'label':_('Top'), 'fieldname':'top', 'fieldtype':'Check','insert_after':'right','description':'For header top'}]
	for r in records:
		create_custom_field('Top Bar Item', r)

def update_social_media_items():
	records = [
		# Website Social Media
		{ 'doctype': 'Website Social Media', 'social_name': _('Instagram'), 'social_icon':'fab fa-instagram', 'social_class':'social-icons-instagram'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Youtube'), 'social_icon':'fab fa-youtube', 'social_class':'social-icons-youtube'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Google Plus'), 'social_icon':'fab fa-google-plus-g', 'social_class':'social-icons-googleplus'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Twitter'), 'social_icon':'fab fa-twitter', 'social_class':'social-icons-twitter'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Facebook'), 'social_icon':'fab fa-facebook-f', 'social_class':'social-icons-facebook'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Pinterest'), 'social_icon':'fab fa-pinterest-p', 'social_class':'social-icons-pinterest'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('LinkedIn'), 'social_icon':'fab fa-linkedin-in', 'social_class':'social-icons-linkedin'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Vimeo'), 'social_icon':'Vimeo', 'social_class':'fa fa-vimeo'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Flickr'), 'social_icon':'Flickr', 'social_class':'fa fa-flickr'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Reddit'), 'social_icon':'fab fa-reddit-alien', 'social_class':'social-icons-reddit'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Tumblr'), 'social_icon':'fab fa-tumblr', 'social_class':'social-icons-tumblr'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Xing'), 'social_icon':'fab fa-xing', 'social_class':'social-icons-xing'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('VK'), 'social_icon':'fab fa-vk', 'social_class':'social-icons-vk'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Email'), 'social_icon':'fas fa-envelope-open-text', 'social_class':'social-icons-email'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('Skype'), 'social_icon':'fab fa-skype', 'social_class':'social-icons-skype'}
		,{ 'doctype': 'Website Social Media', 'social_name': _('RSS'), 'social_icon':'fas fa-rss', 'social_class':'social-icons-rss'}]
	print("Update Website Social Media records")
	make_records(records)

def update_website_background_pattern_items():
		records = [
			# Website Background Pattern
			{ 'doctype': 'Website Background Pattern', 'background_name': 'Gray Jean', 'image':'/assets/publisher/img/patterns/gray_jean.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Linedpaper', 'image':'/assets/publisher/img/patterns/linedpaper.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Az Subtle', 'image':'/assets/publisher/img/patterns/az_subtle.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Blizzard', 'image':'/assets/publisher/img/patterns/blizzard.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Denim', 'image':'/assets/publisher/img/patterns/denim.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Fancy Deboss', 'image':'/assets/publisher/img/patterns/fancy_deboss.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Honey Im Subtle', 'image':'/assets/publisher/img/patterns/honey_im_subtle.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Linen', 'image':'/assets/publisher/img/patterns/linen.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Pw_maze_white', 'image':'/assets/publisher/img/patterns/pw_maze_white.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Skin_side_up', 'image':'/assets/publisher/img/patterns/skin_side_up.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Stitched_wool', 'image':'/assets/publisher/img/patterns/stitched_wool.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Straws', 'image':'/assets/publisher/img/patterns/straws.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Subtle_grunge', 'image':'/assets/publisher/img/patterns/subtle_grunge.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Textured_stripes', 'image':'/assets/publisher/img/patterns/textured_stripes.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Wild_oliva', 'image':'/assets/publisher/img/patterns/wild_oliva.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Worn_dots', 'image':'/assets/publisher/img/patterns/worn_dots.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Bright_squares', 'image':'/assets/publisher/img/patterns/bright_squares.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'Random_grey_variations', 'image':'/assets/publisher/img/patterns/random_grey_variations.png'}
			,{ 'doctype': 'Website Background Pattern', 'background_name': 'books', 'image':'/assets/publisher/img/patterns/books.jpg'}
			]
		print("Update Website Background Pattern records")
		make_records(records)

def update_website_section_theme_items():
	records = [
		# Website Section Theme
		{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-3', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 3 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-4', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 4 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-5', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 5 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-6', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 6 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-7', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 7 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-8', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 8 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-9', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 9 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-1', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 1 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-2', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 2 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-3', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 3 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-4', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 4 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-5', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 5 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-6', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 6 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-7', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 7 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-8', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 8 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-dark-scale-9', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Dark Scale 9 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-tertiary', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Tertiary Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-quaternary', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Quaternary Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'background_image':'/assets/publisher/img/section_img/parallax-hotel.jpg', 'center_aligned':0, 'class_name': 'parallax section-parallax', 'custom_background':'Image', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Default Parallax Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'background_video':'/assets/publisher/img/section_img/memory-of-a-woman.mp4', 'center_aligned':0, 'class_name': 'video section section-text-light section-video', 'custom_background':'Video', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Video Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-1', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 1', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-3', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 3', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-4', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 4', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-5', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 5', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-6', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 6', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-7', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 7', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-8', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 8', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-9', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 9', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-10', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 10', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-1', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 1 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-default bg-color-light-scale-2', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color Light Scale 2 Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'section-secondary', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Secondary Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-grey-scale-2', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Grey Scale 2', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':0, 'class_name': 'bg-color-light', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Color white Section', 'with_divider':0}
		,{ 'doctype': 'Website Section Theme', 'center_aligned':1, 'class_name': 'section-primary', 'custom_background':'', 'removing_margin_top_and_bottom':1, 'removing_top_border':1, 'section_theme_name':'Primary Section', 'with_divider':0}
		]
	print("Update Website Section Theme records")
	make_records(records)

def update_website_theme_settings_standard():
	frappe.flags.in_import = True
	records = [
		# Website Theme Settings
		{ 'doctype': 'Website Theme Settings', 'theme':'Standard', 'custom': 0, 'module':'Publisher Website', 'theme_scss':''}]
	print("Update Website Theme Settings Standard record")
	make_records(records)
	frappe.flags.in_import = False

def update_website_header_design_items():
	records = [
		# Website Header Design
		{ 'doctype': 'Website Header Design', 'header_design_name':'Navbar', 'header_design_url': 'templates/includes/header/navbar/navbar.html'}
		,{ 'doctype': 'Website Header Design', 'header_design_name':'Navbar Center Double', 'header_design_url': 'templates/includes/header/navbar_center_double/navbar.html'}
		]
	print("Update Website Header Design records")
	make_records(records)

def update_website_page_header_design_items():
	records = [
		# Website Page Header Design
		{ 'doctype': 'Website Page Header Design', 'page_header_design_name':'Title Position Center Medium', 'page_header_design_url': 'templates/includes/page_header/title_position_center_medium/breadcrumbs.html'}
		,{ 'doctype': 'Website Page Header Design', 'page_header_design_name':'Title Position Right Small', 'page_header_design_url': 'templates/includes/page_header/title_position_right_small/breadcrumbs.html'}
		]
	print("Update Website Page Header Design records")
	make_records(records)

def make_products_settings():
	# update in Products Settings in settings
	print("Update Products Settings")
	products_settings = frappe.get_doc("Products Settings", "Products Settings")
	products_settings.products_per_page = 12
	products_settings.enable_field_filters = 1
	products_settings.filter_fields = []
	for fieldname in ("item_group", "binding", "subject", "author", "language", "age_range", "grade_range", "series_name", "illustrator", "awards"):
		products_settings.append("filter_fields", {
			"doctype": "Website Filter Field",
			"fieldname": fieldname
		})
	products_settings.save()

def make_website_settings(company):
	# update in home page in settings
	print("Update Website Settings")
	website_settings = frappe.get_doc("Website Settings", "Website Settings")
	website_settings.home_page = 'index'
	website_settings.brand_html = "<img alt='Publisher' width='275' height='40' data-sticky-width='220' data-sticky-height='32'  data-sticky-top='0' src='/assets/publisher/img/logo-publisher.png'>"
	website_settings.favicon = '/assets/publisher/img/publisher-icon.png'
	website_settings.navbar_search = 1
	website_settings.copyright = company
	website_settings.top_bar_items = []
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Home"),
	    "right": 0,
	    "target": "",
	    "top": 0,
	    "url": "/"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("About Us"),
	    "right": 0,
	    "target": "",
	    "top": 0,
	    "url": "/about"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Publication"),
	    "right": 0,
	    "target": "",
	    "top": 0
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("All Books"),
	    "right": 0,
	    "target": "",
	    "top": 0,
	    "url": "/all-books"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Authors"),
	    "right": 1,
	    "target": "",
	    "top": 0,
	    "url": "/authors"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Blog"),
	    "right": 1,
	    "target": "",
	    "top": 0,
	    "url": "/blog"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Contact Us"),
	    "right": 1,
	    "target": "",
	    "top": 0,
	    "url": "/contact"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("New Arrival"),
	    "right": 0,
	    "target": "",
	    "top": 1,
	    "url": "/publication/new-arrival"
	})
	website_settings.append("top_bar_items", {
		"doctype": "Top Bar Item",
		"label": _("Help & FAQs"),
	    "right": 0,
	    "target": "",
	    "top": 1,
	    "url": "/kb/ordering"
	})
	website_settings.footer_items = []
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Get to Know Us")
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Home"),
	    "parent_label": _("Get to Know Us"),
	    "url": "/"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("About Us"),
		"parent_label": _("Get to Know Us"),
		"url": "/about"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Authors"),
	    "parent_label": _("Get to Know Us"),
	    "url": "/authors"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Blog"),
	    "parent_label": _("Get to Know Us"),
	    "url": "/blog"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Contact Us"),
	    "parent_label": _("Get to Know Us"),
	    "url": "/contact"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Books")
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("New Arrival"),
	    "parent_label": _("Books"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Hot Sale"),
	    "parent_label": _("Books"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Audio Books"),
	    "parent_label": _("Books"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Children's Books"),
	    "parent_label": _("Books"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Publication")
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Antiques & Collectibles"),
	    "parent_label": _("Publication"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Architecture"),
	    "parent_label": _("Publication"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Juvenile Fiction"),
	    "parent_label": _("Publication"),
	    "url": "/all-books"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Let Us Help You")
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("My Account"),
	    "parent_label": _("Let Us Help You"),
	    "url": "/login"
	})
	website_settings.append("footer_items", {
		"doctype": "Top Bar Item",
		"label": _("Help"),
	    "parent_label": _("Let Us Help You"),
	    "url": "/kb/ordering"
	})
	website_settings.save()

def update_item_group_items():
	print("Update Item Group records")
	frappe.db.set_value('Item Group', _('Products'), 'show_in_website', 0)
	records = [
		# item group
		{'doctype': 'Item Group', 'item_group_name': _('Publication'),
			'is_group': 1, 'parent_item_group': _('All Item Groups'), "show_in_website": 1},
		{'doctype': 'Item Group', 'item_group_name': _('New Arrival'),
			'is_group': 0, 'parent_item_group': _('Publication'), "show_in_website": 1 }
		]

	make_records(records)


def update_publisher_website_settings(confirm,company,language):
	# update in Publisher Website Settings
	idx_en = 1
	idx_ar = 2
	if language == 'ar':
		idx_en = 2
		idx_ar = 1
	publisher_website_settings = frappe.get_doc("Publisher Website Settings", "Publisher Website Settings")
	publisher_website_settings.website_theme_settings = 'Standard'
	publisher_website_settings.website_header_design = 'Navbar Center Double'
	publisher_website_settings.website_page_header_design = 'Title Position Right Small'
	publisher_website_settings.website_page_header_design = 'Title Position Right Small'
	if language == 'en':
		publisher_website_settings.publication_item_group = _("Publication")

	publisher_website_settings.all_data_added_to_publisher = 1 if language == 'en' else 0
	publisher_website_settings.example_data_updated = 1 if confirm else 0
	publisher_website_settings.allow_payment_image_in_footer = 1 if confirm else 0
	publisher_website_settings.display_social_links_on_footer = 1
	publisher_website_settings.website_social_media_item = []
	publisher_website_settings.append("website_social_media_item", {
		"doctype": "Website Social Media Item",
		"social_class": "social-icons-facebook",
	    "social_icon": "fab fa-facebook-f",
	    "social_name": "Facebook",
	    "social_url": "#",
	    "social_url_target": "_blank"
	})
	publisher_website_settings.append("website_social_media_item", {
		"doctype": "Website Social Media Item",
		"social_class": "social-icons-linkedin",
	    "social_icon": "fab fa-linkedin-in",
	    "social_name": "LinkedIn",
	    "social_url": "#",
	    "social_url_target": "_blank"
	})
	publisher_website_settings.append("website_social_media_item", {
		"doctype": "Website Social Media Item",
		"social_class": "social-icons-twitter",
	    "social_icon": "fab fa-twitter",
	    "social_name": "Twitter",
	    "social_url": "#",
	    "social_url_target": "_blank"
	})
	publisher_website_settings.append("website_social_media_item", {
		"doctype": "Website Social Media Item",
		"social_class": "Email",
	    "social_icon": "fas fa-envelope-open-text",
	    "social_name": "social-icons-email",
	    "social_url": "mailto:",
	    "social_url_target": ""
	})
	publisher_website_settings.all_books_page_title = _('All Books')
	publisher_website_settings.website_languages = []
	publisher_website_settings.append("website_languages", {
		"doctype": "Website Languages",
		"language": "en",
	    "language_flag": "us",
	    "language_name": "English",
		"allow_display_contact_on_footer": 1,
	    "allow_top_bar_notice": 0,
	    "copyright": company,
	    "footer_address_details": "4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE",
	    "footer_address_title": "Address",
	    "footer_company_information_title": "Contact Info",
	    "footer_email_details": "support@publisher.ae",
	    "footer_email_title": "Email:",
	    "footer_newsletter_details": "Get all the latest information on Books, Sign up for newsletter today.",
	    "footer_newsletter_input_title": "Enter your email address...",
	    "footer_newsletter_send_button_title": "Send Email",
	    "footer_newsletter_title": "Subscribe Newsletter",
	    "footer_social_media_title": "Stay Connected",
	    "footer_tel_details": "(+1)866-540-3229",
	    "footer_tel_title": "Call us now:",
	    "main_page_title": company,
	    "idx": idx_en ,
	    "top_bar_notice": "<p class=\"text-color-light font-weight-semibold mb-0\">\nGet Up to <strong>30% OFF</strong> New-Arrival books \n<a href=\"publication/new-arrival\" class=\"btn btn-primary-scale-2 btn-modern btn-px-2 btn-py-1 ml-2\">Check Now</a>  \n<span class=\"opacity-6 text-1\">* Limited time only.</span>\n</p>",
	    "top_header_message": "FREE RETURNS, STANDARD SHIPPING ORDERS $99+"
	})
	publisher_website_settings.append("website_languages", {
		"doctype": "Website Languages",
		"allow_display_contact_on_footer": 1,
	    "footer_tel_title": "\u0647\u0627\u062a\u0641",
	    "language": "ar",
	    "language_flag": "ae",
	    "allow_top_bar_notice": 0,
	    "copyright": company,
	    "footer_address_details": "30 \u0634 \u0627\u0644\u062d\u0645\u062f , \u0627\u0628\u0648\u0638\u0628\u064a, \u0627\u0644\u0627\u0645\u0627\u0631\u0627\u062a \u0627\u0644\u0639\u0631\u0628\u064a\u0629 \u0627\u0644\u0645\u062a\u062d\u062f\u0629",
	    "footer_address_title": "\u0639\u0646\u0648\u0627\u0646",
	    "footer_company_information_title": "\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0627\u0644\u0627\u062a\u0635\u0627\u0644",
	    "footer_email_details": "support@publisher.com",
	    "footer_email_title": "\u0628\u0631\u064a\u062f \u0627\u0644\u0643\u062a\u0631\u0648\u0646\u064a",
	    "footer_newsletter_details": "\u0627\u062d\u0635\u0644 \u0639\u0644\u0649 \u0623\u062d\u062f\u062b \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u062d\u0648\u0644 \u0627\u0644\u0643\u062a\u0628 \u060c \u0627\u0634\u062a\u0631\u0643 \u0641\u064a \u0627\u0644\u0646\u0634\u0631\u0629 \u0627\u0644\u0625\u062e\u0628\u0627\u0631\u064a\u0629 \u0627\u0644\u064a\u0648\u0645.",
	    "footer_newsletter_input_title": "\u0623\u062f\u062e\u0644 \u0639\u0646\u0648\u0627\u0646 \u0628\u0631\u064a\u062f\u0643 \u0627\u0644\u0627\u0644\u0643\u062a\u0631\u0648\u0646\u064a...",
	    "footer_newsletter_send_button_title": "\u0627\u0634\u062a\u0631\u0627\u0643",
	    "footer_newsletter_title": "\u0627\u0634\u062a\u0631\u0643 \u0641\u064a \u0627\u0644\u0646\u0634\u0631\u0629 \u0627\u0644\u0625\u062e\u0628\u0627\u0631\u064a\u0629",
	    "footer_social_media_title": "\u0627\u0628\u0642 \u0639\u0644\u0649 \u0627\u062a\u0635\u0627\u0644",
	    "footer_tel_details": "(+1)866-540-3229",
	    "language_name": "\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
	    "main_page_title": company,
	    "idx": idx_ar ,
	    "top_bar_notice": "",
	})
	publisher_website_settings.save()

def update_website_section_items(confirm):
	records = [
		# Website Section
		{'doctype': 'Website Section', 'name': _('Who We Are'), 'no_of_columns': '2', 'section_based_on': 'Cards', 'show_section_title': 0, 'section_cards':[{'image': '/assets/publisher/img/section_img/32.jpg', 'image_type': 'Full photo', 'route': '/about', 'show_card_title': 0, 'text_center_aligned': 1,'title': _('About Publisher')}, {'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras volutpat id sapien ac varius. Fusce hendrerit ligula a con.', 'image_type': '', 'route': '/about', 'show_card_title': 1, 'text_center_aligned': 0, 'title': _('We are sure you will enjoy work with us and our team.')}]
		}]
	if confirm:
		records +=[
			{"doctype": "Website Section", "name": _("Why Choose Us?"), "no_of_columns": "3", "section_based_on": "Cards" ,"show_section_title": 1, "section_cards": [
			{ "content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Recusandae aliquam numquam, aspernatur expedita ipsa molestiae."), "icon": "fas fa-book", "image_type": "Icon", "route": "/about", "show_card_title": 1, "subtitle": _("First Publication"), "text_center_aligned": 0, "title": _("Books")}
			, {"content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi incidunt voluptatem, suscipit, dignissimos voluptas sint."), "icon": "fas fa-chalkboard-teacher", "image_type": "Icon", "route": "/about", "show_card_title": 1, "subtitle": _("Best Team Work"), "text_center_aligned": 0, "title": _("Process")}
			,{ "content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Adipisci, libero blanditiis voluptatum ratione at, necessitatibus!"), "icon": "fas fa-users", "image_type": "Icon", "route": "/author", "show_card_title": 1, "subtitle": "Very Famous", "text_center_aligned": 0, "title": "Authors"}
			]}
			,{ "doctype": "Website Section", "name": _("We Can Help You"), "no_of_columns": "3", "section_based_on": "Cards", "show_section_title": 1 , "section_cards": [
		     {"content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Recusandae aliquam numquam, aspernatur expedita ipsa molestiae."), "icon": "fas fa-book", "image_type": "Icon", "route": "/about", "show_card_title": 1, "subtitle": _("First Publication"), "text_center_aligned": 1, "title": _("Books")},
		     {"content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Animi incidunt voluptatem, suscipit, dignissimos voluptas sint."), "icon": "fas fa-chalkboard-teacher", "image_type": "Icon", "route": "/about", "show_card_title": 1,  "subtitle": _("Best Team Work"), "text_center_aligned": 1, "title": _("Process")}
			 ,{ "content": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Adipisci, libero blanditiis voluptatum ratione at, necessitatibus!"), "icon": "fas fa-users", "image_type": "Icon", "route": "/author", "show_card_title": 1, "subtitle": _("Very Famous"), "text_center_aligned": 1, "title": _("Authors")}
			 ]}
			 ,{"doctype": "Website Section", "name": _("Best Books"), "no_of_columns": "2", "section_based_on": "Cards","show_section_title": 0, "section_cards": [
		      {"content": "", "icon": "", "image": "/assets/publisher/img/section_img/8a0ed77.jpg", "image_type": "Full photo", "route": "/about", "show_card_title": 0, "subtitle": "", "text_center_aligned": 0, "title": _("Books")},
		      { "content": "", "icon": "", "image": "/assets/publisher/img/section_img/9.jpg", "image_type": "Full photo", "route": "/about", "show_card_title": 0, "subtitle": "", "text_center_aligned": 0, "title": _("Process")}
		     ]}
			]
	print("Update Website Section records")
	make_records(records)

def update_author_items():
	records = [
		# Author
		{"doctype": "Author", "author_name": "J. K. Rowling", "description": "J.K. Rowling is the author of the record-breaking, multi-award-winning Harry Potter novels. Loved by fans around the world, the series has sold more than 500 million copies, been translated into 80 languages and made into eight blockbuster films.\n\nShe has written three companion volumes in aid of charity: Quidditch Through the Ages and Fantastic Beasts and Where to Find Them (in aid of Comic Relief and Lumos), and The Tales of Beedle the Bard (in aid of Lumos).\n\nIn 2012, J.K. Rowling's digital company and digital publisher Pottermore was launched, a place where fans can enjoy the latest news from across the wizarding world, features and original writing by J.K. Rowling.\n\nHer first novel for adult readers, The Casual Vacancy, was published in September 2012 and adapted for TV by the BBC in 2015. J.K. Rowling also writes crime novels under the pseudonym Robert Galbraith, featuring private detective Cormoran Strike. The first four novels The Cuckoo's Calling (2013), The Silkworm (2014), Career of Evil (2015) and Lethal White (2018) all topped the national and international bestseller lists. The first three have been adapted for television, produced by Bront\u00eb Film and Television.\n\nJ.K. Rowling's 2008 Harvard commencement speech was published in 2015 as an illustrated book, Very Good Lives: The Fringe Benefits of Failure and the Importance of Imagination, and sold in aid of Lumos and university-wide financial aid at Harvard.\n\nIn 2016, J.K. Rowling collaborated with writer Jack Thorne and director John Tiffany on the stage play Harry Potter and the Cursed Child Parts One and Two, which is now running at The Palace Theatre in London's West End and at The Lyric Theatre on Broadway.\n\nAlso in 2016, J.K. Rowling made her screenwriting debut with the film Fantastic Beasts and Where to Find Them. A prequel to the Harry Potter series, this new adventure of Magizoologist Newt Scamander marked the start of a five-film series to be written by the author. The second film in the series, Fantastic Beasts: The Crimes of Grindelwald was released in November 2018.\n\nThe script book of the play Harry Potter and the Cursed Child Parts One and Two was published in 2016. The original screenplays of the Fantastic Beasts films are published too: Fantastic Beasts and Where to Find Them (2016) and Fantastic Beasts: The Crimes of Grindelwald (2018).\n\nAs well as receiving an OBE and Companion of Honour for services to children's literature, J.K. Rowling has received many awards and honours, including France's L\u00e9gion d'Honneur and the Hans Christian Andersen Award.\n\nwww.jkrowling.com\n\nImage: Photography Debra Hurford Brown \u00a9 J.K. Rowling 2018", "image": "/assets/publisher/img/section_img/fvh43djng407r1iq142ng0sk5f._US230_.jpg", "name": "j-k-rowling", "show_in_website": 1, 	"author_social_media": [
	   {"social_class": "social-icons-facebook","social_icon": "fab fa-facebook-f","social_name": "Facebook","social_url": "https://www.facebook.com/JKRowling", "social_url_target": "_blank"}
	   ,{"social_class": "social-icons-twitter", "social_icon": "fab fa-twitter", "social_name": "Twitter", "social_url": "https://twitter.com/jk_rowling", "social_url_target": "_blank"}
	  ]}
	  ,{"doctype": "Author", "author_name": "Ishmael Beah", "description": "Ishmael Beah, born in Sierra Leone, West Africa, is the # 1 New York Times & international bestselling author of \"A Long Way Gone, Memoirs of a Boy Soldier\" & \"Radiance of Tomorrow, A Novel.\" His books have been published in over 40 languages and won numerous prestigious awards and reviews. His Memoir was nominated for a Quill Award in the Best Debut Author category for 2007. Time Magazine named the book as one of the Top 10 Nonfiction books of 2007, ranking at number 3. Carolyn See from The Washington Post wrote, \"Everyone in the world should read this book... We should read it to learn about the world and about what it means to be human.\"\n\nHis novel, written with the gentle lyricism of a dream and the moral clarity of a fable is a powerful book about preserving what means the most to us, even in uncertain times.\nThe New York Times finds in his writing an \"allegorical richness\" and a \"remarkable humanity to his characters\". His forthcoming book \"Little Family, A Novel\" will be published in April 28, 2020 by Riverhead Books (Penguin USA).\n\nHe is a UNICEF Goodwill Ambassador and advocate for Children by War, and a member of the Human Rights Watch Children Advisory Committed. He lives in Los Angeles, California with his wife and three children.", "image": "/assets/publisher/img/section_img/71mYq44oWKL._US230_.jpg", "name": "ishmael-beah", "show_in_website": 1}
	  ,{"doctype": "Author", "author_name": "Barbara Delinsky", "description": "Barbara Delinsky, author of A WEEK AT THE SHORE (May 2020), BEFORE AND AGAIN (2018), BLUEPRINTS (2015), SWEET SALT AIR (2013), ESCAPE (2011), and NOT MY DAUGHTER (2010), has written twenty-five New York Times bestsellers, with many more of her books on other national bestseller lists. There are nearly forty million copies of her books in print, including those published in thirty languages worldwide.\n\nBarbara's fiction centers upon everyday families facing not-so-everyday challenges. She is particularly drawn to exploring themes of motherhood, marriage, sibling rivalry, and friendship.\n\nA lifelong New Englander, Barbara earned a B.A. in Psychology at Tufts University and an M.A. in Sociology at Boston College. As a breast cancer survivor who lost her mother to the disease when she was only eight, Barbara compiled the non-fiction book Uplift: Secrets from the Sisterhood of Breast Cancer Survivors, a handbook of practical tips and upbeat anecdotes. She donates her proceeds from the sale of this book to her charitable foundation, which funds an ongoing research fellowship at Massachusetts General Hospital.\n\nBarbara enjoys knitting, photography, and cats. She also loves to interact with her readers through her website at www.barbaradelinsky.com, on Facebook at www.facebook.com/bdelinsky, on Instagram at https://www.instagram.com/barbaradelinsky/, and on Twitter as @BarbaraDelinsky.","image": "/assets/publisher/img/section_img/51N++YskolL._US230_.jpg", "name": "barbara-delinsky", "show_in_website": 1, "author_social_media": [
	  {"social_class": "social-icons-facebook", "social_icon": "fab fa-facebook-f", "social_name": "Facebook", "social_url": "https://www.facebook.com/bdelinsky", "social_url_target": "_blank"}
	  ,{"social_class": "social-icons-instagram", "social_icon": "fab fa-instagram", "social_name": "Instagram", "social_url": "https://www.instagram.com/barbaradelinsky/", "social_url_target": "_blank"}
	  ,{"social_class": "social-icons-twitter", "social_icon": "fab fa-twitter", "social_name": "Twitter", "social_url": "https://twitter.com/BarbaraDelinsky", "social_url_target": "_blank"}
	  ]}
	  ]
	print("Update Author records")
	make_records(records)

def update_website_slideshow():
	records = [
		# Website Slideshow
		{"doctype": "Website Slideshow","name": "Full Page", "slideshow_name": "Full Page" ,"slideshow_items": [
	     {"description": _("Get your books in Order and Accessories"), "heading": _("Do IT Yourself "), "image": "/assets/publisher/img/section_img/10.jpg", "link_path": "/about", "link_target": "", "link_title": _("Read More"), "set_position": "Left"}
		 ,{"description": _("Up to 50 %"), "heading": _("Huge Sale"), "image": "/assets/publisher/img/section_img/101a00e.jpg", "link_path": "/all-books", "link_target": "", "link_title": _("Shop now"), "set_position": "Left"}
		 ,{"description": _("Get your books in Order and Accessories"), "heading": _("We Can Help"), "image": "/assets/publisher/img/section_img/2.jpg", "link_path": "/contact", "link_target": "", "link_title": _("Contact Us Today!"),"set_position": "Left"}
	    ]}
		,{"doctype": "Website Slideshow", "slideshow_name": "Harry Potter and the Deathly Hallows", "name": "Harry Potter and the Deathly Hallows", "slideshow_items": [{"image": "/assets/publisher/img/section_img/511DhzIj4cL.jpg"},{"image": "/assets/publisher/img/section_img/71sH3vxziLL.jpg"},{"image": "/assets/publisher/img/section_img/519jtgrWA4L.jpg"},{"image": "/assets/publisher/img/section_img/51lEfwiV3OL.jpg"},{"image": "/assets/publisher/img/section_img/41b6lTH9JaL.jpg"},{"image": "/assets/publisher/img/section_img/174909_v9_bb.jpg"}
	    ]}
	  ]
	print("Update Website Slideshow records")
	make_records(records)

def update_item_group_extra_items():
	records = [
		# item group
		{'doctype': 'Item Group', 'item_group_name': _('Antiques & Collectibles'),
			'is_group': 1, 'parent_item_group': _('Publication'), "show_in_website": 1},
		{'doctype': 'Item Group', 'item_group_name': _('Clocks & Watches'),
			'is_group': 0, 'parent_item_group': _('Antiques & Collectibles'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Comics'),
			'is_group': 0, 'parent_item_group': _('Antiques & Collectibles'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Sports Cards'),
			'is_group': 0, 'parent_item_group': _('Antiques & Collectibles'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Transportation'),
			'is_group': 0, 'parent_item_group': _('Antiques & Collectibles'), "show_in_website": 1 },

		{'doctype': 'Item Group', 'item_group_name': _('Architecture'),
			'is_group': 1, 'parent_item_group': _('Publication'), "show_in_website": 1},
		{'doctype': 'Item Group', 'item_group_name': _('Buildings'),
			'is_group': 0, 'parent_item_group': _('Architecture'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Interior Design'),
			'is_group': 0, 'parent_item_group': _('Architecture'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('International Architecture'),
			'is_group': 0, 'parent_item_group': _('Architecture'), "show_in_website": 1 },

		{'doctype': 'Item Group', 'item_group_name': _('Graphic Novels and Comics'),
			'is_group': 1, 'parent_item_group': _('Publication'), "show_in_website": 1},
		{'doctype': 'Item Group', 'item_group_name': _('Anthologies'),
			'is_group': 0, 'parent_item_group': _('Graphic Novels and Comics'), "show_in_website": 1 },

		{'doctype': 'Item Group', 'item_group_name': _('Juvenile Fiction'),
			'is_group': 1, 'parent_item_group': _('Publication'), "show_in_website": 1},
		{'doctype': 'Item Group', 'item_group_name': _('Color Theory'),
			'is_group': 0, 'parent_item_group': _('Juvenile Fiction'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Fashion'),
			'is_group': 0, 'parent_item_group': _('Juvenile Fiction'), "show_in_website": 1 },
		{'doctype': 'Item Group', 'item_group_name': _('Film & Video'),
			'is_group': 0, 'parent_item_group': _('Juvenile Fiction'), "show_in_website": 1 }
		]
	print("Update extra Item Group records")
	make_records(records)

def update_binding_items():
	# Binding
	records = [{"doctype":"Binding", "binding_name": _(d)} for d in ('Trade Paperback','Hardcover')]
	print("Update Binding records")
	make_records(records)

def update_publication_language_items():
	# Publication Language
	records = [{"doctype":"Publication Language", "language_name": _(d)} for d in ('Arabic','English')]
	print("Update Publication Language records")
	make_records(records)

def update_publication_subject_items():
	# Publication Subject
	records = [{"doctype":"Publication Subject", "subject": _(d)} for d in ('Fantasy fiction','Children s-Science Fiction and Fantasy', 'England')]
	print("Update Publication Subject records")
	make_records(records)

def update_illustrator_items():
	# Illustrator
	records = [{"doctype":"Illustrator", "illustrator_name": _("Mary Grandpr\u00e9")}]
	print("Update Illustrator records")
	make_records(records)

def update_publication_series_items():
	# Publication Series
	records = [{"doctype":"Publication Series", "series_name": _('Harry Potter')}]
	print("Update Publication Series records")
	make_records(records)

def update_publication_age_range_items():
	# Publication Age Range
	records = [{"doctype":"Publication Age Range", "age_range": _(d)} for d in ('0 to 2','3 to 5','6 to 7','8 to 10','11 to 13','14 and up')]
	print("Update Publication Age Range records")
	make_records(records)

def update_publication_grade_range_items():
	# Publication Grade Range
	records = [{"doctype":"Publication Grade Range", "grade_range": _('4 to 10')}]
	print("Update Publication Grade Range records")
	make_records(records)

def update_publication_award_items():
	# Publication Award
	records = [{"doctype":"Publication Award", "award_title": _('Pulitzer Prize for Fiction')}]
	print("Update Publication Award records")
	make_records(records)

def update_item_items(default_warehouse):
	# Item
	if default_warehouse:
		records = [{"doctype":"Item", "item_code": _("Harry Potter and the Philosopher's Stone"), 'item_name':_("Harry Potter and the Philosopher's Stone"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51UoqRAxwEL.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 147.35,"publication_date": "1998-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 17, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 1, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Chamber of Secrets"), 'item_name':_("Harry Potter and the Chamber of Secrets"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51TA3VfN8RL.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 159.65,"publication_date": "1999-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 19, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 2, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Prisoner of Azkaban"), 'item_name':_("Harry Potter and the Prisoner of Azkaban"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51Dfqo6jR5L._SX331_BO1,204,203,200_.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 165.95,"publication_date": "2000-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 23, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 3, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Goblet of Fire"), 'item_name':_("Harry Potter and the Goblet of Fire"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51Vjb2qJwzL._SX331_BO1,204,203,200_.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 173.35,"publication_date": "2000-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 24, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 4, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Order of the Phoenix"), 'item_name':_("Harry Potter and the Order of the Phoenix"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51-SI2+aQ2L._SX331_BO1,204,203,200_.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 180.45,"publication_date": "2000-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 17, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 5, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Half-Blood Prince"), 'item_name':_("Harry Potter and the Half-Blood Prince"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/51myHyjJsyL._SX331_BO1,204,203,200_.jpg", "valuation_rate": 127.0, "opening_stock": 200.0, "standard_rate": 227.35,"publication_date": "2000-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 20, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 6, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse, "website_item_groups": [{ "item_group": _("Film & Video")}] }

		,{"doctype":"Item", "item_code": _("Harry Potter and the Deathly Hallows"), 'item_name':_("Harry Potter and the Deathly Hallows"),"item_group": _("New Arrival"), "stock_uom": "Nos", "image": "/assets/publisher/img/section_img/511DhzIj4cL.jpg", "valuation_rate": 127.0, "opening_stock": 249.0, "standard_rate": 227.35,"publication_date": "2000-01-10", "author": _("j-k-rowling"), "binding": _("Hardcover"), "age_range": _("6 to 7"), "pages": 398, "number_of_units": 20, "publication_height_in": 0.0, "publication_thickness": 0.0, "publication_width_in": 0.0, "illustration": 1, "illustrator": _("Mary Grandpr\u00e9"), "series": 1, "series_name": _("Harry Potter"), "series_number": 7, "subject": [{"publication_subject": _("Children s-Science Fiction and Fantasy")}, { "publication_subject": _("Fantasy fiction")}],"awards": [{"publication_award": _("Pulitzer Prize for Fiction")}],"show_in_website": 1, "website_warehouse": default_warehouse,"slideshow": "Harry Potter and the Deathly Hallows", "website_item_groups": [{ "item_group": _("Film & Video")}] }
		]
		print("Update Item records")
		make_records(records)
	else:
		print("Unable update Item records Default Warehouse unset")

def update_website_homepage_settings(confirm,default_language=None,ignor_language=False):
		# update in home page in settings
		print("Update Website Homepage Settings")
		website_homepage_settings = frappe.get_doc("Website Homepage Settings", "Website Homepage Settings")
		website_homepage_settings.title = _('Home')
		website_homepage_settings.section_item = []
		if default_language == 'en' or ignor_language:
			website_homepage_settings.append("section_item", {
				"doctype": "Website Homepage Section Item",
				"section_type": 'Website Section',
				"section_theme": 'Color white Section',
				"website_section": _("Who We Are")
			})
		website_homepage_settings.author_section_title = _('Author Best Selling')
		website_homepage_settings.allow_blog_section = 0
		website_homepage_settings.blog_section_title = _("Blog")
		website_homepage_settings.blog_section_description = _("Authors, readers, critics, media − and booksellers.")
		if confirm:
			website_homepage_settings.slideshow = 'Full Page'
			website_homepage_settings.author = 'j-k-rowling'
			website_homepage_settings.display_after_section_item_row_number = 4
			website_homepage_settings.append("section_item", {
				"doctype": "Website Homepage Section Item",
				"section_type": 'Item Group',
				"section_theme": 'Tertiary Section',
				"item_group_name": _("New Arrival"),
				"display_item_group_as":"Slider",
				"number_of_columns_item":5
			})
			website_homepage_settings.append("section_item", {
				"doctype": "Website Homepage Section Item",
				"section_type": 'Website Section',
				"section_theme": 'Color Light Scale 1 Section',
				"website_section": _("We Can Help You")
			})
			website_homepage_settings.append("section_item", {
				"doctype": "Website Homepage Section Item",
				"section_type": 'Item Group',
				"section_theme": 'Tertiary Section',
				"item_group_name": _("Film & Video"),
				"display_item_group_as":"Grid",
				"number_of_columns_item":4,
				"max_number_to_display_item_group":12
			})
			website_homepage_settings.append("section_item", {
				"doctype": "Website Homepage Section Item",
				"section_type": 'Website Section',
				"section_theme": 'Color Light Section',
				"website_section": _("Best Books")
			})
		website_homepage_settings.save()

def update_website_authors_settings(confirm):
	# update in Website Authors Settings
	print("Update Website Authors Settings")
	website_authors_settings = frappe.get_doc("Website Authors Settings", "Website Authors Settings")
	website_authors_settings.title = _('Authors')
	website_authors_settings.author_publication_title = _('Publications')
	website_authors_settings.authors_per_page = 12
	website_authors_settings.no_of_columns = 4
	website_authors_settings.introduction = "<div><span style=\"background-color: rgb(255, 255, 255); color: rgb(129, 136, 152);\">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magnam, tempora assumenda esse eveniet. Dolor velit fuga nam sequi dicta iusto, fugiat in esse facilis pariatur architecto voluptatem reprehenderit hic ipsa sint nihil, ea quidem porro praesentium. Distinctio fugiat natus voluptatem sit dignissimos quia aliquam cumque perferendis doloremque quidem vero error ratione iste voluptas, nam adipisci nemo?</span></div>"
	website_authors_settings.introduction_ar = "<div><span style=\"background-color: rgb(255, 255, 255); color: rgb(129, 136, 152);\">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magnam, tempora assumenda esse eveniet. Dolor velit fuga nam sequi dicta iusto, fugiat in esse facilis pariatur architecto voluptatem reprehenderit hic ipsa sint nihil, ea quidem porro praesentium. Distinctio fugiat natus voluptatem sit dignissimos quia aliquam cumque perferendis doloremque quidem vero error ratione iste voluptas, nam adipisci nemo?</span></div>"
	website_authors_settings.save()

def update_website_about_us_settings(confirm):
	# update in Website About Us Settings
	print("Update Website About Us Settings")
	website_about_us_settings = frappe.get_doc("Website About Us Settings", "Website About Us Settings")
	website_about_us_settings.title = _('About Us')
	website_about_us_settings.company_introduction = "<div><span style=\"background-color: rgb(255, 255, 255); color: rgb(129, 136, 152);\">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magnam, tempora assumenda esse eveniet. Dolor velit fuga nam sequi dicta iusto, fugiat in esse facilis pariatur architecto voluptatem reprehenderit hic ipsa sint nihil, ea quidem porro praesentium. Distinctio fugiat natus voluptatem sit dignissimos quia aliquam cumque perferendis doloremque quidem vero error ratione iste voluptas, nam adipisci nemo?</span></div>"
	website_about_us_settings.company_introduction_ar = "<div><span style=\"background-color: rgb(255, 255, 255); color: rgb(129, 136, 152);\">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magnam, tempora assumenda esse eveniet. Dolor velit fuga nam sequi dicta iusto, fugiat in esse facilis pariatur architecto voluptatem reprehenderit hic ipsa sint nihil, ea quidem porro praesentium. Distinctio fugiat natus voluptatem sit dignissimos quia aliquam cumque perferendis doloremque quidem vero error ratione iste voluptas, nam adipisci nemo?</span></div>"
	website_about_us_settings.no_of_columns = 3
	website_about_us_settings.no_of_columns_about_item = 2
	website_about_us_settings.company_history_heading = _("Our History")
	website_about_us_settings.company_history_image = '/assets/publisher/img/section_img/our-history-1.jpg'
	website_about_us_settings.team_members_heading = _('Meet our Team of Specialists')
	website_about_us_settings.team_members_description = _('We love everything about books')
	website_about_us_settings.no_of_columns_member_item = 4
	if confirm:
		website_about_us_settings.about_us_counters_items = []
		website_about_us_settings.append("about_us_counters_items", {
			'doctype':'About Us Counters Items',
			"data_from": 0,
			"data_to": 20,
		    "icon": "<i class=\"fas fa-star\"></i>"
			,"show_plus": 0,
		    "title": _("Years in Business")
		})
		website_about_us_settings.append("about_us_counters_items", {
			'doctype':'About Us Counters Items',
			"data_from": 0,
		    "data_to": 22000,
		    "icon": "<i class=\"fas fa-book\"></i>",
			"show_plus": 1,
		    "title": _("Published Books")
		})
		website_about_us_settings.append("about_us_counters_items", {
			'doctype':'About Us Counters Items',
			"data_from": 0,
		    "data_to": 1000,
		    "icon": "<i class=\"fas fa-user\"></i>",
			"show_plus": 1,
		    "title": _("Authors")
		})

		website_about_us_settings.about_us_vision_items = []
		website_about_us_settings.append("about_us_vision_items", {
			'doctype':'About Us Vision Items',
			"description": _("Major Views"),
		    "details": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est quas dicta exercitationem deleniti molestiae, voluptatum harum modi eius officia nulla quaerat ex asperiores ullam numquam amet provident incidunt sapiente, vero dolorum, sunt omnis deserunt ea dolores ratione suscipit. Veritatis."),
		    "icon": "/assets/publisher/img/section_img/custom-icon-1.png",
			"title": _("Our Vision")
		})
		website_about_us_settings.append("about_us_vision_items", {
			'doctype':'About Us Vision Items',
			"description": _("Our Aims"),
		    "details": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores nobis dolorum sint! Dolorem aperiam voluptatum doloribus nulla quo libero? At, asperiores, fuga! Minus quo ad nam cupiditate quis natus, ut tempore, culpa sunt?"),
		    "icon": "/assets/publisher/img/section_img/custom-icon-2.png",
			"title": _("Our Mission")
		})


		website_about_us_settings.company_history_description = _("Our Way of Success")
		website_about_us_settings.company_history_details = _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Praesentium iste necessitatibus velit eum quis, dignissimos modi atque libero magni, explicabo nihil illo soluta accusantium suscipit, nobis maiores deleniti mollitia, quod id nam assumenda ducimus.")
		website_about_us_settings.company_history = []
		website_about_us_settings.append("company_history", {
			'doctype':'About Us Company History',
			"highlight": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Corporis, rem labore facere. Veritatis enim laborum facilis minima, illo ratione?"),
			"title": _("Company formed"),
		    "year": "2008"
		})
		website_about_us_settings.append("company_history", {
			'doctype':'About Us Company History',
			"highlight": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ad cum eos quas, explicabo, possimus harum optio consequuntur quod veniam."),
			"title": _("Suspendisse tincidunt nibh."),
		    "year": "2014"
		})
		website_about_us_settings.append("company_history", {
			'doctype':'About Us Company History',
			"highlight": _("Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, molestias numquam culpa, eligendi debitis dicta, hic delectus obcaecati accusantium quaerat magni explicabo et dolorem mollitia cumque sint deserunt. Labore vel magnam quasi."),
			"title": _("Awards and 300 empolyees"),
		    "year": "2020"
		})

		website_about_us_settings.team_members = []
		website_about_us_settings.append("team_members", {
			'doctype':'About Us Team Member',
			"bio": _("CEO"),
		    "full_name": _("John Doe"),
		    "image_link": "/assets/publisher/img/section_img/team-1.jpg"
		})
		website_about_us_settings.append("team_members", {
			'doctype':'About Us Team Member',
			"bio": _("Director of Investments"),
		    "full_name": _("Tom Doe"),
		    "image_link": "/assets/publisher/img/section_img/team-2.jpg"
		})
		website_about_us_settings.append("team_members", {
			'doctype':'About Us Team Member',
			"bio": _("Chief officer"),
		    "full_name": _("Josh Doe"),
		    "image_link": "/assets/publisher/img/section_img/team-3.jpg"
		})
		website_about_us_settings.append("team_members", {
			'doctype':'About Us Team Member',
			"bio": _("Risk Analyst"),
		    "full_name": _("Alan Doe"),
		    "image_link": "/assets/publisher/img/section_img/team-4.jpg"
		})

	website_about_us_settings.save()

def update_website_contact_us_settings(confirm):
	# update in Website Contact Us Settings
	print("Update Website Contact Us Settings")
	website_contact_us_settings = frappe.get_doc("Website Contact Us Settings", "Website Contact Us Settings")
	website_contact_us_settings.title = _('Contact Us')
	website_contact_us_settings.contact_info_heading = _("Contact Info")
	website_contact_us_settings.no_of_columns = 4
	website_contact_us_settings.branches_info_heading = _("Branches Info")
	website_contact_us_settings.number_of_columns_item = 4
	website_contact_us_settings.form_title = _("Send a Message")
	website_contact_us_settings.query_options = _('General')
	if confirm:
		website_contact_us_settings.google_map = '<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 480px; border: 0;\" width=\"100%\"></iframe>'
		website_contact_us_settings.contact_info_description = _("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed imperdiet libero id nisi euismod, sed porta est consectetur. Vestibulum auctor felis eget orci semper vestibulum. Pellentesque ultricies nibh gravida, accumsan libero luctus, molestie nunc.")
		website_contact_us_settings.contact_info_items = []
		website_contact_us_settings.append("contact_info_items", {
			'doctype':'Contact Us Info Items',
			"details": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
			"icon": "/assets/publisher/img/section_img/icon-location.svg",
		    "link_target": "",
			"title": _("Address")
		})
		website_contact_us_settings.append("contact_info_items", {
			'doctype':'Contact Us Info Items',
			"details": "(800) 123-4567",
		    "details_link": "tel:+1234567890",
		    "icon": "/assets/publisher/img/section_img/icon-phone.svg",
		    "link_target": "",
			"title": _("Phone Number")
		})
		website_contact_us_settings.append("contact_info_items", {
			'doctype':'Contact Us Info Items',
			"details": "support@publisher.ae",
		    "details_link": "mailto:support@publisher.ae",
		    "icon": "/assets/publisher/img/section_img/icon-envelope.svg",
		    "link_target": "",
			"title": _("E-mail Address")
		})
		website_contact_us_settings.append("contact_info_items", {
			'doctype':'Contact Us Info Items',
			"details": _("Mon - Sun / 9:00AM - 8:00PM"),
			"icon": "/assets/publisher/img/section_img/icon-calendar.svg",
		    "link_target": "",
			"title": _("Working Days/Hours")
		})

		website_contact_us_settings.branches_info_description = _("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed imperdiet libero id nisi euismod, sed porta est consectetur. Vestibulum auctor felis eget orci semper vestibulum. Pellentesque ultricies nibh gravida, accumsan libero luctus, molestie nunc.")
		website_contact_us_settings.branches_info__items = []
		website_contact_us_settings.append("branches_info__items", {
			'doctype':'Contact Us Branches Items',
			"address": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
		    "email": "info@publisher.ae",
		    "google_map": "<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 200px; border: 0;\" width=\"100%\"></iframe>",
			"tel": "8001234567",
		    "title": _("Dubai")
		})
		website_contact_us_settings.append("branches_info__items", {
			'doctype':'Contact Us Branches Items',
			"address": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
		    "email": "info@publisher.ae",
		    "google_map": "<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 200px; border: 0;\" width=\"100%\"></iframe>",
			"tel": "8001234567",
		    "title": _("Cairo")
		})
		website_contact_us_settings.append("branches_info__items", {
			'doctype':'Contact Us Branches Items',
			"address": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
		    "email": "info@publisher.ae",
		    "google_map": "<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 200px; border: 0;\" width=\"100%\"></iframe>",
			"tel": "8001234567",
		    "title": _("New York")
		})
		website_contact_us_settings.append("branches_info__items", {
			'doctype':'Contact Us Branches Items',
			"address": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
		    "email": "info@publisher.ae",
		    "google_map": "<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 200px; border: 0;\" width=\"100%\"></iframe>",
			"tel": "8001234567",
		    "title": _("Tokyo")
		})
		website_contact_us_settings.append("branches_info__items", {
			'doctype':'Contact Us Branches Items',
			"address": _("4 Khalidya Tower, AlKhalidya - Abu Dhabi, UAE"),
		    "email": "info@publisher.ae",
		    "google_map": "<iframe allowfullscreen=\"\" class=\"google-ma h-100 mb-0\" frameborder=\"0\" src=\"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3631.2071517958234!2d54.3524392154647!3d24.478278366495637!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e5e6673b232294f%3A0xb37bb78014c0caf7!2sKhalidiya%20Tower%20-%20Al%20Hisn%20-%20Abu%20Dhabi%20-%20United%20Arab%20Emirates!5e0!3m2!1sen!2seg!4v1603170063526!5m2!1sen!2seg\" style=\"min-height: 200px; border: 0;\" width=\"100%\"></iframe>",
			"tel": "8001234567",
		    "title": _("Alex")
		})
		website_contact_us_settings.form_description = _("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla volutpat ex finibus urna tincidunt, auctor ullamcorper risus luctus.")

	website_contact_us_settings.save()

def update_shopping_cart_settings():
	print("Update allow show price of items")
	shopping_cart_settings = frappe.get_doc("Shopping Cart Settings", "Shopping Cart Settings")
	shopping_cart_settings.show_price = 1

	shopping_cart_settings.save()
