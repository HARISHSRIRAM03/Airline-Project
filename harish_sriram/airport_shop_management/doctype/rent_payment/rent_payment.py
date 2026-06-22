# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentPayment(Document):
	def before_insert(self):
		if not self.amount:
			shop = frappe.get_doc("Shop", self.shop)
			self.amount = shop.rent_amount

	def before_submit(self):
		if not self.paid_date:
			self.paid_date = frappe.utils.nowdate()
