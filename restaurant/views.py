
# File: views.py
# Author: Daniel Arteaga (dany@bu.edu), 9/12/2025
# Description: Django views for the restaurant web application, 
# including main page, order form, and order confirmation logic.

from django.shortcuts import render
import random
import time

def main(request):
    """Render the main restaurant page with location, hours, and an image."""
    template_name = "restaurant/main.html"

    # Restaurant image URL to display on the main page
    RESTAURANT_IMAGE_URL = "https://margs.com/wp-content/uploads/2024/06/Margs-Woodbridge-Interior.jpg"

    context = {
        'restaurant_img': RESTAURANT_IMAGE_URL
    }

    return render(request, template_name, context)

def order(request):
    """Render the order form page with a randomly selected daily special."""
    template_name = "restaurant/order.html"

    # List of daily specials (name and price)
    DAILY_SPECIALS = [
        {"name": "Mole Poblano", "price": 12.00},
        {"name": "Pozole", "price": 14.00},
        {"name": "Cochinita Pibil", "price": 10.50},
    ]

    # Randomly select a daily special for the order form
    daily_special = random.choice(DAILY_SPECIALS)

    context = {
        'daily_special': daily_special
    }

    return render(request, template_name, context)


def confirmation(request):
    """Process the submitted order and render the confirmation page with order details."""
    template_name = "restaurant/confirmation.html"

    if request.method == "POST":
        # Retrieve customer information from the form
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        # Menu items and their prices (USD)
        MENU_ITEMS = {
            'Tacos': 5.00,
            'Burrito': 7.50,
            'Enchiladas': 6.00,
            'Nachos': 3.00
        }

        # Determine which menu items were ordered
        ordered_items = []  # List of ordered item names
        total_price = 0  # Total price of the order
        for item_name, item_price in MENU_ITEMS.items():
            # Check if the item was selected in the form
            if request.POST.get(item_name):
                ordered_items.append(item_name)
                total_price += item_price

        # Add daily special if selected
        if request.POST.get('daily_special'):
            daily_special_name = request.POST.get('daily_special_name', '')
            daily_special_price = float(request.POST.get('daily_special_price', 0))
            ordered_items.append(daily_special_name)
            total_price += daily_special_price

        # Calculate the ready time for the order
        timezone_offset_seconds = -4 * 3600
        current_time_seconds = time.time() + timezone_offset_seconds
        # Add a random preparation time between 30 and 60 minutes
        ready_time_seconds = current_time_seconds + random.randint(30, 60) * 60
        ready_time = time.strftime("%I:%M %p", time.localtime(ready_time_seconds))

        context = {
            'name': customer_name,
            'phone': customer_phone,
            'email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time
        }

        return render(request, template_name, context)

    # If not a POST request, just render the confirmation page
    return render(request, template_name)