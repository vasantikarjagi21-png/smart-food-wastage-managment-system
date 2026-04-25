from django.contrib import admin
from django.urls import path
from foodsystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('meal/', views.meals, name='meal'),
    path('inventory/', views.inventory, name='inventory'),
    path('waste/', views.waste, name='waste'),
    path('donation/', views.donation, name='donation'),

    path('qr/', views.qr_page, name='qr'),
    path('save_qr/', views.save_qr, name='save_qr'),
]