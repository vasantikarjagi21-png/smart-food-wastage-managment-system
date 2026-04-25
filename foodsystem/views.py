from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from datetime import date, timedelta


# 🏠 HOME PAGE
def home(request):
    return render(request, 'home.html')


# 🔐 LOGIN
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            return redirect('/dashboard/')   # ✅ go to dashboard

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


from datetime import date, timedelta
from django.shortcuts import render, redirect

def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    if request.session.get('role') != 'admin':
        return redirect('/meal/')

    today = date.today()
    week_ago = today - timedelta(days=7)

    MealBooking.objects.filter(date=today)
    MealBooking.objects.filter(date__gte=week_ago)

    # ✅ Total counts
    meal_count = MealBooking.objects.count()
    waste_count = Waste.objects.count()
    inventory = Inventory.objects.count()
    donations = Donation.objects.count()

    # ✅ Meal type counts (TOTAL)
    breakfast_count = MealBooking.objects.filter(meal_type__iexact="Breakfast").count()
    lunch_count = MealBooking.objects.filter(meal_type__iexact="Lunch").count()
    dinner_count = MealBooking.objects.filter(meal_type__iexact="Dinner").count()

    # ✅ TODAY counts (SAFE for DateField)
    today_breakfast = MealBooking.objects.filter(date=today, meal_type__iexact="Breakfast").count()
    today_lunch = MealBooking.objects.filter(date=today, meal_type__iexact="Lunch").count()
    today_dinner = MealBooking.objects.filter(date=today, meal_type__iexact="Dinner").count()

    # ✅ WEEKLY counts
    week_breakfast = MealBooking.objects.filter(date__gte=week_ago, meal_type__iexact="Breakfast").count()
    week_lunch = MealBooking.objects.filter(date__gte=week_ago, meal_type__iexact="Lunch").count()
    week_dinner = MealBooking.objects.filter(date__gte=week_ago, meal_type__iexact="Dinner").count()

    # ✅ Efficiency
    if (meal_count + waste_count) > 0:
        efficiency = (meal_count / (meal_count + waste_count)) * 100
    else:
        efficiency = 0

    # 🔥 IMPORTANT: send table data to dashboard
    meals = MealBooking.objects.all().order_by('-id')

    return render(request, 'dashboard.html', {
        'meal_count': meal_count,
        'waste': waste_count,
        'inventory': inventory,
        'donations': donations,
        'efficiency': round(efficiency, 2),

        # meal types total
        'breakfast_count': breakfast_count,
        'lunch_count': lunch_count,
        'dinner_count': dinner_count,

        # today
        'today_breakfast': today_breakfast,
        'today_lunch': today_lunch,
        'today_dinner': today_dinner,

        # weekly
        'week_breakfast': week_breakfast,
        'week_lunch': week_lunch,
        'week_dinner': week_dinner,

        # 🔥 ADD THIS (VERY IMPORTANT FOR TABLE)
        'meals': meals
    })
# 🍽 MEAL BOOKING (✅ FIXED)
def meal(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    if request.method == "POST":
        user = User.objects.get(id=request.session.get('user_id'))
        meal_type = request.POST.get('meal_type')

        MealBooking.objects.create(
            user=user,
            date=date.today(),
            meal_type=meal_type
        )

        return redirect('/dashboard/')   # ✅ correct redirect

    return render(request, 'meal.html')


# 📦 INVENTORY
def inventory(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    if request.session.get('role') != 'admin':
        return redirect('/no-access/')

    if request.method == "POST":
        Inventory.objects.create(
            item_name=request.POST.get('name'),
            quantity=int(request.POST.get('qty')),
            expiry_date=request.POST.get('exp')
        )
        return redirect('/inventory/')

    items = Inventory.objects.all()
    alerts = [i for i in items if i.expiry_date and i.expiry_date <= date.today()]

    return render(request, 'inventory.html', {
        'items': items,
        'alerts': alerts
    })


# 🗑 WASTE
def waste(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    if request.session.get('role') != 'admin':
        return redirect('/no-access/')

    waste_items = Waste.objects.all()

    return render(request, 'waste.html', {
        'waste_items': waste_items
    })


# 🤝 DONATION
def donation(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    if request.method == "POST":
        Donation.objects.create(
            ngo_name=request.POST.get('ngo'),
            food_item=request.POST.get('food'),
            quantity=request.POST.get('qty') or 1
        )

    donations = Donation.objects.all()

    return render(request, 'donation.html', {
        'donations': donations
    })


# 📷 QR PAGE
def qr_page(request):
    if not request.session.get('user_id'):
        return redirect('/login/')

    return render(request, 'qr.html')


# 📷 SAVE QR
def save_qr(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get('code')

        if code:
            ScanLog.objects.create(code=code)

        return JsonResponse({'status': 'success'})


# 🚪 LOGOUT
def logout(request):
    request.session.flush()
    return redirect('/')