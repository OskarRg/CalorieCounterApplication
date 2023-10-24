from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    meal_name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbs = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.meal_name


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
dates = Date.objects.annotate(
    total_calories=Sum("meals__calories"), # dodaje pole total_calories z sumą kalorii z posiłków
    total_protein=Sum("meals__protein"), # dodaje pole total_protein z sumą białka z posiłków
    total_fat=Sum("meals__fat"), # dodaje pole total_fat z sumą tłuszczu z posiłków
    total_carbs=Sum("meals__carbs") # dodaje pole total_carbs z sumą węglowodanów z posiłków
)
"""