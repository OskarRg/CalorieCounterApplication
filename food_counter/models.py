from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    calories = models.FloatField()  # changed
    protein = models.FloatField()  # changed
    fat = models.FloatField()  # changed
    carbs = models.FloatField()  # changed
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, null=True, default=1)

    def __str__(self):
        return f"{self.product_name} (100 g) - {self.calories:.2f} kcal P: {self.protein:.2f} F: {self.fat:.2f} C: {self.carbs:.2f}"


class ProductMeal(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)


class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    calories = models.FloatField()  # changed
    protein = models.FloatField()  # changed
    fat = models.FloatField()  # changed
    carbs = models.FloatField()  # changed
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # new
    grams = models.PositiveIntegerField(default=100)
    products = models.ManyToManyField(Products, through=ProductMeal, blank=True) # tutaj używamy argumentu through

    def save(self, *args, **kwargs):
        # metoda, która jest wywoływana po zapisaniu obiektu Meal
        self.calories = 0.0 # zerujemy pole calories i zmieniamy typ na float
        self.protein = 0.0 # zerujemy pole protein i zmieniamy typ na float
        self.fat = 0.0 # zerujemy pole fat i zmieniamy typ na float
        self.carbs = 0.0 # zerujemy pole carbs i zmieniamy typ na float
        super().save(*args, **kwargs) # wywołujemy metodę nadrzędną, która zapisuje obiekt Meal w bazie danych
        for product_meal in self.productmeal_set.all(): # pętla po wszystkich obiektach ProductMeal powiązanych z tym posiłkiem
            self.calories += product_meal.product.calories * self.grams / 100 # dodajemy iloczyn kalorii i gramów produktu do pola calories posiłku
            self.protein += product_meal.product.protein * self.grams / 100 # analogicznie dla białka
            self.fat += product_meal.product.fat * self.grams / 100 # analogicznie dla tłuszczu
            self.carbs += product_meal.product.carbs * self.grams / 100 # analogicznie dla węglowodanów
        super().save(*args, **kwargs) # wywołujemy metodę nadrzędną, która zapisuje obiekt Meal w bazie danych

    def __str__(self):
        # Nadpisujemy metodę __str__, aby zwracała nazwę i gramaturę posiłku
        return f"{self.meal_name} ({self.grams} g) - {self.calories:.2f} kcal P: {self.protein:.2f} F: {self.fat:.2f} C: {self.carbs:.2f}"


class Date(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_calories = models.FloatField(default=0)  # changed
    total_protein = models.FloatField(default=0)  # changed
    total_fat = models.FloatField(default=0)  # changed
    total_carbs = models.FloatField(default=0)  # changed
    meals = models.ManyToManyField(Meal, blank=True)

    def save(self, *args, **kwargs):
        # metoda, która jest wywoływana po zapisaniu obiektu Date
        self.total_calories = 0.0  # zerujemy pole total_calories i zmieniamy typ na float
        self.total_protein = 0.0  # zerujemy pole total_protein i zmieniamy typ na float
        self.total_fat = 0.0  # zerujemy pole total_fat i zmieniamy typ na float
        self.total_carbs = 0.0  # zerujemy pole total_carbs i zmieniamy typ na float
        super().save(*args, **kwargs)  # wywołujemy metodę nadrzędną, która zapisuje obiekt Date w bazie danych
        for meal in self.meals.all():  # pętla po wszystkich posiłkach przypisanych do tej daty
            self.total_calories += meal.calories  # dodajemy wartość pola calories posiłku do pola total_calories daty
            self.total_protein += meal.protein  # dodajemy wartość pola protein posiłku do pola total_protein daty
            self.total_fat += meal.fat  # dodajemy wartość pola fat posiłku do pola total_fat daty
            self.total_carbs += meal.carbs  # dodajemy wartość pola carbs posiłku do pola total_carbs daty
        super().save(*args, **kwargs)  # wywołujemy metodę nadrzędną, która zapisuje obiekt Date w bazie danych

    def __str__(self):
        return str(self.total_calories)

    def get_absolute_url(self):
        return reverse('date-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['user', 'date']


# ZAMIANA NA FLOAT
"""
class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbs = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)  # new
    grams = models.PositiveIntegerField(default=100)  # new

    def __str__(self):
        return self.meal_name


class Products(models.Model):
    product_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbs = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name


class Date(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_calories = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    total_fat = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    meals = models.ManyToManyField(Meal, blank=True)

    def save(self, *args, **kwargs):
        # metoda, która jest wywoływana po zapisaniu obiektu Date
        self.total_calories = 0  # zerujemy pole total_calories
        self.total_protein = 0  # zerujemy pole total_protein
        self.total_fat = 0  # zerujemy pole total_fat
        self.total_carbs = 0  # zerujemy pole total_carbs
        super().save(*args, **kwargs)  # wywołujemy metodę nadrzędną, która zapisuje obiekt Date w bazie danych
        for meal in self.meals.all():  # pętla po wszystkich posiłkach przypisanych do tej daty
            self.total_calories += meal.calories  # dodajemy wartość pola calories posiłku do pola total_calories daty
            self.total_protein += meal.protein  # dodajemy wartość pola protein posiłku do pola total_protein daty
            self.total_fat += meal.fat  # dodajemy wartość pola fat posiłku do pola total_fat daty
            self.total_carbs += meal.carbs  # dodajemy wartość pola carbs posiłku do pola total_carbs daty
        super().save(*args, **kwargs)  # wywołujemy metodę nadrzędną, która zapisuje obiekt Date w bazie danych

    def __str__(self):
        return str(self.total_calories)

    def get_absolute_url(self):
        return reverse('date-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['user', 'date']
"""

"""
dates = Date.objects.annotate(
    total_calories=Sum("meals__calories"), # dodaje pole total_calories z sumą kalorii z posiłków
    total_protein=Sum("meals__protein"), # dodaje pole total_protein z sumą białka z posiłków
    total_fat=Sum("meals__fat"), # dodaje pole total_fat z sumą tłuszczu z posiłków
    total_carbs=Sum("meals__carbs") # dodaje pole total_carbs z sumą węglowodanów z posiłków
)
"""
