import frappe
from harish_sriram.www.shops_css import get_shops_css

def get_context(context):
    context.shops = frappe.get_all(
        "Shop",
        fields=["name", "shop_name", "shop_type", "airport", "area_sq_ft", "rent_amount", "status"],
        order_by="creation desc"
    )
    context.title = "Available Shops"
    context.css = get_shops_css()
