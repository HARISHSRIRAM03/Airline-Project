// Copyright (c) 2026, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop", {
	refresh(frm) {
		if (frm.doc.status === "Occupied" && frm.doc.tenant) {
			frm.add_custom_button(__("Collect Rent"), () => {
				frappe.new_doc("Rent Payment", {
					shop: frm.doc.name,
					tenant: frm.doc.tenant,
					airport: frm.doc.airport,
					amount: frm.doc.rent_amount,
				});
			});
		}
	},
});
