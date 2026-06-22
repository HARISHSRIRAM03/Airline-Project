# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart = get_chart(data)
	report_summary = get_report_summary(data)

	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{
			"fieldname": "airline",
			"label": _("Airline"),
			"fieldtype": "Link",
			"options": "Airline",
			"width": 200,
		},
		{
			"fieldname": "revenue",
			"label": _("Revenue"),
			"fieldtype": "Currency",
			"width": 150,
		},
	]


def get_data():
	data = frappe.db.sql(
		"""
		SELECT
			airline.name AS airline,
			COALESCE(SUM(ticket.total_amount), 0) AS revenue
		FROM `tabAirline` airline
		LEFT JOIN `tabAirplane` airplane
			ON airplane.airline = airline.name
		LEFT JOIN `tabAirplane Flight` flight
			ON flight.airplane = airplane.name
		LEFT JOIN `tabAirplane Ticket` ticket
			ON ticket.flight = flight.name AND ticket.docstatus = 1
		GROUP BY airline.name
		ORDER BY revenue DESC
		""",
		as_dict=True,
	)

	return data


def get_chart(data):
	labels = [d.airline for d in data]
	values = [d.revenue for d in data]

	return {
		"data": {
			"labels": labels,
			"datasets": [{"name": _("Revenue"), "values": values}],
		},
		"type": "donut",
		"height": 300,
	}


def get_report_summary(data):
	total_revenue = sum(d.revenue for d in data)

	return [
		{
			"value": total_revenue,
			"indicator": "Green",
			"label": _("Total Revenue"),
			"datatype": "Currency",
		},
	]
