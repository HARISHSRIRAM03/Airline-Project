# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Shop(Document):
	def before_save(self):
		if not self.rent_amount:
			default_rent = frappe.db.get_single_value("Airport Shop Settings", "default_rent_amount")
			if default_rent:
				self.rent_amount = default_rent

	def before_insert(self):
		self.status = "Available"
