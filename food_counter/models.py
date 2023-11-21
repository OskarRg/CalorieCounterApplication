from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, null=True, default=1)

    def __str__(self):
        return f"{self.product_name} (100 g) - {self.calories:.2f} kcal P: {self.protein:.2f} F: {self.fat:.2f} C: {self.carbs:.2f}"


class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    grams = models.PositiveIntegerField(default=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=False)

    def save(self, *args, **kwargs):
        self.calories = self.product.calories * self.grams / 100
        self.protein = self.product.protein * self.grams / 100
        self.fat = self.product.fat * self.grams / 100
        self.carbs = self.product.carbs * self.grams / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.meal_name} ({self.grams} g) - {self.calories:.2f} kcal P: {self.protein:.2f} F: {self.fat:.2f} C: {self.carbs:.2f}"


class Date(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_calories = models.FloatField(default=0)
    total_protein = models.FloatField(default=0)
    total_fat = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)
    meals = models.ManyToManyField(Meal, blank=True)

    def save(self, *args, **kwargs):
        self.total_calories = 0.0
        self.total_protein = 0.0
        self.total_fat = 0.0
        self.total_carbs = 0.0
        super().save(*args, **kwargs)
        for meal in self.meals.all():
            self.total_calories += meal.calories
            self.total_protein += meal.protein
            self.total_fat += meal.fat
            self.total_carbs += meal.carbs
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f"{self.total_calories} kcal")

    def get_absolute_url(self):
        return reverse('date-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['user', 'date']