import frappe


def create_default_shop_types():
    types = ["Stall", "Walk-through", "Normal"]
    for shop_type in types:
        if not frappe.db.exists("Shop Type", shop_type):
            doc = frappe.new_doc("Shop Type")
            doc.shop_type_name = shop_type
            doc.enabled = 1
            doc.insert()
