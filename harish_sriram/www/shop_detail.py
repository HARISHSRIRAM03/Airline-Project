import frappe
from harish_sriram.www.shops_css import get_shops_css

def get_context(context):
    shop_name = frappe.form_dict.get("shop")
    if not shop_name:
        frappe.local.flags.redirect_location = "/shops"
        raise frappe.Redirect

    shop = frappe.get_doc("Shop", shop_name)
    context.shop = shop
    context.title = shop.shop_name
    context.css = get_shops_css()
    context.submitted = frappe.form_dict.get("submitted") == "1"
