from django.contrib import admin
from django.urls import path
from foodsystem import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌐 Home
    path('', views.home, name='home'),

    # 🔐 Login
    path('login/', views.login, name='login'),

    # 📊 Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # 🍽 Meal Booking
    path('meal/', views.meal, name='meal'),

    # 📦 Inventory
    path('inventory/', views.inventory, name='inventory'),

    # 🗑 Waste Tracking
    path('waste/', views.waste, name='waste'),

    # 🤝 Donation
    path('donation/', views.donation, name='donation'),

    # 📷 QR Scanner
    path('qr/', views.qr_page, name='qr'),
    path('save_qr/', views.save_qr, name='save_qr'),

    #logout
    path('logout/', views.logout),
]