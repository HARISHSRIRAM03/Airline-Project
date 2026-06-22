# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		add_ons: DF.Table
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport_code: DF.Data
		duration_of_flight: DF.Duration | None
		flight: DF.Link
		flight_price: DF.Currency
		gate_number: DF.Data | None
		passenger: DF.Link
		source_airport_code: DF.Data
		status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency
	# end: auto-generated types

	def validate(self):
		if self.flight:
			flight_doc = frappe.get_doc("Airplane Flight", self.flight)
			if not self.source_airport_code:
				self.source_airport_code = flight_doc.source_airport_code
			if not self.destination_airport_code:
				self.destination_airport_code = flight_doc.destination_airport_code
		self.validate_capacity()
		self.calculate_total_amount()

	def validate_capacity(self):
		if not self.flight:
			return
		flight_doc = frappe.get_doc("Airplane Flight", self.flight)
		airplane_doc = frappe.get_doc("Airplane", flight_doc.airplane)
		capacity = airplane_doc.capacity

		filters = {"flight": self.flight, "docstatus": ["!=", 2]}
		if self.name:
			filters["name"] = ["!=", self.name]
		ticket_count = frappe.db.count("Airplane Ticket", filters)

		if ticket_count >= capacity:
			frappe.throw(
				f"Flight {self.flight} is fully booked. "
				f"Airplane {airplane_doc.name} has only {capacity} seats "
				f"and {ticket_count} tickets have already been issued."
			)

	def calculate_total_amount(self):
		total = self.flight_price
		for item in self.add_ons:
			total += item.amount
		self.total_amount = total
