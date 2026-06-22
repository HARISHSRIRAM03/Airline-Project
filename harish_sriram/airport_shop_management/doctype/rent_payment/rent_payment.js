// Copyright (c) 2026, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rent Payment", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Rent Receipt"), () => {
				frappe.set_route("print", frm.doc.doctype, frm.doc.name);
			}, __("Print"));
		}
	},
});
