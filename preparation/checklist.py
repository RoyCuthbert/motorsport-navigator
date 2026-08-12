from .models import PreparationItem

DEFAULT_CHECKLIST = {

    "Vehicle": [
        "Check engine oil",
        "Check coolant",
        "Check brake fluid",
        "Check clutch fluid",
        "Check power steering fluid",
        "Check battery",
        "Check lights",
        "Check wipers",
        "Check tyre pressures",
        "Torque wheel nuts",
        "Check wheel bearings",
        "Check suspension",
        "Check brakes",
    ],

    "Safety": [
        "Helmet",
        "HANS Device",
        "Race Suit",
        "Gloves",
        "Boots",
        "Fire Extinguisher",
        "First Aid Kit",
        "Spill Kit",
        "Tow Rope",
        "Warning Triangle",
    ],

    "Documents": [
        "Driving Licence",
        "Competition Licence",
        "Club Membership",
        "Vehicle Logbook",
        "Insurance",
        "MOT",
        "Event Signing-On",
    ],

    "Tools": [
        "Socket Set",
        "Spanners",
        "Screwdrivers",
        "Torque Wrench",
        "Jack",
        "Axle Stands",
        "Wheel Brace",
        "Cable Ties",
        "Duct Tape",
        "Electrical Tape",
        "Jump Leads",
        "Fuel Can",
        "Funnels",
        "Spare Fluids",
    ],

}




def create_default_checklist(user, event):

    # An event must have a competition vehicle
    if not event.vehicle:
        return

    # Don't create duplicate preparation items
    if PreparationItem.objects.filter(
        user=user,
        event=event,
    ).exists():
        return

    # Create a fresh checklist for this event
    for category, items in DEFAULT_CHECKLIST.items():

        for item in items:

            PreparationItem.objects.create(
                user=user,
                event=event,
                vehicle=event.vehicle,
                category=category,
                item=item,
                completed=False,
            )