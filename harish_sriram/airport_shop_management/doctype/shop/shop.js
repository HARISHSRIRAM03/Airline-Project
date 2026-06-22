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
    shop_type(frm) {
        if (frm.doc.shop_type) {
            frappe.db.get_value("Shop Type", frm.doc.shop_type, "enabled", (r) => {
                if (r && !r.enabled) {
                    frappe.msgprint(__("Selected shop type is disabled. Please choose an enabled shop type."));
                    frm.set_value("shop_type", null);
                }
            });
        }
    },
});

frappe.ui.form.on("Shop", {
    setup(frm) {
        frm.set_query("shop_type", function () {
            return {
                filters: { enabled: 1 },
            };
        });
    },
});
