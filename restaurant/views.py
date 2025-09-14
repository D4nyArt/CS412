from django.shortcuts import render
#from django.http import HttpResponse
import random
import time

# Create your views here.

def main(request):
    """View for the main page"""

    template_name = "restaurant/main.html"

    IMG_URL = "https://margs.com/wp-content/uploads/2024/06/Margs-Woodbridge-Interior.jpg"

    context = {
        'restaurant_img': IMG_URL
    }
    
    return render(request, template_name, context)

def order(request):
    """View for placing an order"""

    template_name = "restaurant/order.html"
    daily_specials = [
        {"name": "Mole Poblano", "price": 12.00},
        {"name": "Pozole", "price": 14.00},
        {"name": "Cochinita Pibil", "price": 10.50},

    ]
    daily_special = random.choice(daily_specials)

    context = {
        'daily_special': daily_special
    }

    return render(request, template_name, context)

def confirmation(request):
    """View for submitting an order"""

    template_name = "restaurant/confirmation.html"

    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        # Menu items and their prices
        menu_items = {
            'Tacos': 5.00,
            'Burrito': 7.50,
            'Enchiladas': 6.00,
            'Nachos': 3.00
        }

        # Determine ordered items
        ordered_items = []
        total_price = 0
        for item, price in menu_items.items():
            if request.POST.get(item):
                ordered_items.append(item)
                total_price += price

        # Add daily special if selected
        if request.POST.get('daily_special'):
            daily_special_name = request.POST.get('daily_special_name', '')
            daily_special_price = float(request.POST.get('daily_special_price', 0))
            ordered_items.append(daily_special_name)
            total_price += daily_special_price

        # Calculate ready time
        timezone_offset = -4 * 3600  # Offset in seconds (-4 hours for EST)
        current_time = time.time() + timezone_offset
        ready_time_seconds = current_time + random.randint(30, 60) * 60
        ready_time = time.strftime("%I:%M %p", time.localtime(ready_time_seconds))

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time
        }

        return render(request, template_name, context)

    return render(request, template_name)