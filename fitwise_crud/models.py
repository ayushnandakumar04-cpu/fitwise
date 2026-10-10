from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Foodlog(models.Model):
    title=models.CharField(max_length=200)
    calories=models.PositiveIntegerField(default=0)
    MEAL_TYPE = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE
    )

    service_size=models.CharField(max_length=200)


    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="food_logs")

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.food_name