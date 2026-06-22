import frappe
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@frappe.whitelist()
def get_nearby_restaurants(lat, lon):

    restaurants = frappe.get_all(
        "Restaurant",
        filters={"is_active": 1},
        fields=[
            "name",
            "restaurant_name",
            "latitude",
            "longitude",
            "delivery_radius"
        ]
    )

    result = []

    for r in restaurants:

        distance = calculate_distance(
            float(lat),
            float(lon),
            float(r.latitude),
            float(r.longitude)
        )

        if distance <= float(r.delivery_radius):

            r["distance"] = round(distance, 2)

            result.append(r)

    return result