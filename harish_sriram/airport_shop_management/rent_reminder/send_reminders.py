# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate, format_date


def send_rent_reminders():
	enabled = frappe.db.get_single_value("Airport Shop Settings", "enable_rent_reminders")
	if not enabled:
		return

	shops = frappe.get_all("Shop", filters={"status": "Occupied", "tenant": ["!=", ""]}, fields=["name", "shop_name", "tenant", "rent_amount"])

	for shop in shops:
		tenant = frappe.get_doc("Tenant", shop.tenant)
		if not tenant.email:
			continue

		month_name = frappe.utils.formatdate(nowdate(), "MMMM")
		year = frappe.utils.formatdate(nowdate(), "yyyy")

		existing = frappe.db.exists("Rent Payment", {
			"shop": shop.name,
			"month": month_name,
			"year": int(year),
			"docstatus": 1,
		})
		if existing:
			continue

		subject = f"Rent Reminder - {shop.shop_name} ({month_name} {year})"
		message = f"""
Dear {tenant.tenant_name},

This is a reminder that the rent for your shop <b>{shop.shop_name}</b> at <b>{shop.airport}</b> is due for the month of {month_name} {year}.

Rent Amount: {frappe.utils.fmt_money(shop.rent_amount)}

Please make the payment at your earliest convenience.

Thank you,
Airport Management
"""
		try:
			frappe.sendmail(
				recipients=[tenant.email],
				subject=subject,
				message=message,
			)
		except Exception as e:
			frappe.log_error(f"Failed to send rent reminder to {tenant.email}: {e}", "Rent Reminder")
