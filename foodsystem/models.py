from django.db import models


# 👤 USER MODEL
class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


# 🍽 MEAL BOOKING
class MealBooking(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)

    def __str__(self):
        return f"{self.user.name} - {self.meal_type} ({self.date})"


# 📦 INVENTORY
class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.item_name


# 🗑 WASTE TRACKING
class Waste(models.Model):
    CATEGORY_CHOICES = [
        ('Edible', 'Edible'),
        ('Inedible', 'Inedible'),
    ]

    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='waste/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} ({self.category})"


# 🤝 NGO DONATION
class Donation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    ngo_name = models.CharField(max_length=100)
    food_item = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.ngo_name} - {self.food_item}"


# 📷 QR SCAN LOG
class ScanLog(models.Model):
    code = models.CharField(max_length=200)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


# 📊 REPORTS (FOR ANALYTICS)
class Report(models.Model):
    total_meals = models.IntegerField()
    total_waste = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.date}"


# ⚠ EXPIRY ALERT SYSTEM
class Alert(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message