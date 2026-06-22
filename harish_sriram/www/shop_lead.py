import frappe
from harish_sriram.www.shops_css import get_shops_css

def get_context(context):
    shop_name = frappe.form_dict.get("shop")
    context.shop = None
    if shop_name and frappe.db.exists("Shop", shop_name):
        context.shop = frappe.get_doc("Shop", shop_name)

    if frappe.request.method == "POST":
        lead_name = frappe.form_dict.get("lead_name")
        email = frappe.form_dict.get("email")
        phone = frappe.form_dict.get("phone")
        message = frappe.form_dict.get("message")
        shop = frappe.form_dict.get("shop")

        if not lead_name or not shop:
            context.error = "Name and Shop are required."
        else:
            lead = frappe.get_doc({
                "doctype": "Shop Lead",
                "shop": shop,
                "lead_name": lead_name,
                "email": email,
                "phone": phone,
                "message": message,
            })
            lead.insert(ignore_permissions=True)
            frappe.db.commit()
            frappe.local.flags.redirect_location = f"/shop_detail?shop={shop}&submitted=1"
            raise frappe.Redirect

    context.title = "Submit Interest"
    context.css = get_shops_css()
    context.csrf_token = frappe.sessions.get_csrf_token()
