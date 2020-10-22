# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe, os, json ,click

from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.utils import cstr, getdate


def add_examples():
	default_warehouse = frappe.db.get_single_value('Stock Settings', 'default_warehouse')

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

	update_website_section_items()
	update_website_homepage_settings()
	update_website_about_us_settings()
	update_website_contact_us_settings()


	frappe.db.commit()


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
	make_records(records)

def update_binding_items():
	# Binding
	records = [{"doctype":"Binding", "binding_name": _(d)} for d in ('Trade Paperback','Hardcover')]
	make_records(records)

def update_publication_language_items():
	# Publication Language
	records = [{"doctype":"Publication Language", "language_name": _(d)} for d in ('Arabic','English')]
	make_records(records)

def update_publication_subject_items():
	# Publication Subject
	records = [{"doctype":"Publication Subject", "subject": _(d)} for d in ('Fantasy fiction','Children s-Science Fiction and Fantasy', 'England')]
	make_records(records)

def update_illustrator_items():
	# Illustrator
	records = [{"doctype":"Illustrator", "illustrator_name": _("Mary Grandpr\u00e9")}]
	make_records(records)

def update_publication_series_items():
	# Publication Series
	records = [{"doctype":"Publication Series", "series_name": _('Harry Potter')}]
	make_records(records)

def update_publication_age_range_items():
	# Publication Age Range
	records = [{"doctype":"Publication Age Range", "age_range": _(d)} for d in ('0 to 2','3 to 5','6 to 7','8 to 10','11 to 13','14 and up')]
	make_records(records)

def update_publication_grade_range_items():
	# Publication Grade Range
	records = [{"doctype":"Publication Grade Range", "grade_range": _('4 to 10')}]
	make_records(records)

def update_publication_award_items():
	# Publication Award
	records = [{"doctype":"Publication Award", "award_title": _('Pulitzer Prize for Fiction')}]
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
		make_records(records)


def update_website_section_items():
	records =[
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
	make_records(records)

def update_website_homepage_settings():
		# update in home page in settings
		website_homepage_settings = frappe.get_doc("Website Homepage Settings", "Website Homepage Settings")
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

def update_website_about_us_settings():
	# update in Website About Us Settings
	website_about_us_settings = frappe.get_doc("Website About Us Settings", "Website About Us Settings")
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

def update_website_contact_us_settings():
	# update in Website Contact Us Settings
	website_contact_us_settings = frappe.get_doc("Website Contact Us Settings", "Website Contact Us Settings")
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
