import frappe

def get_context(context):
    context.airlines = frappe.get_all("Airline", fields=["name", "founding_year", "customer_care_number", "headquarters"])

    context.airplanes = frappe.get_all("Airplane", fields=["name", "model", "airline", "capacity"], order_by="airline")

    context.airports = frappe.get_all("Airport", fields=["name", "code", "city", "country"])

    context.passengers = frappe.get_all("Flight Passenger", fields=["name", "first_name", "last_name", "date_of_birth"])

    context.tickets = frappe.get_all("Airplane Ticket", fields=["name", "flight", "passenger", "source_airport_code", "destination_airport_code", "departure_date", "status"])

    context.airline_stats = []
    for airline in context.airlines:
        count = frappe.db.count("Airplane", {"airline": airline.name})
        context.airline_stats.append({"name": airline.name, "count": count})

    context.total_airlines = len(context.airlines)
    context.total_airplanes = len(context.airplanes)
    context.total_tickets = len(context.tickets)
    context.total_airports = len(context.airports)
    context.total_passengers = len(context.passengers)

    context.title = "Airline Portal"
