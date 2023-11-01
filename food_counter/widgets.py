from django.forms import CheckboxSelectMultiple
from .models import Meal


class MealCheckboxSelectMultiple(CheckboxSelectMultiple):
    # Klasa widgetu, która dodaje informację o gramaturze do etykiety posiłku
    def format_value(self, value):
        # Metoda, która zwraca listę wartości do wyświetlenia na widżecie
        if not isinstance(value, (tuple, list)):
            value = [value]
        values = []
        for v in value:
            # Dla każdej wartości znajdujemy odpowiadający jej obiekt Meal
            meal = Meal.objects.get(id=v)
            # Dodajemy do listy wartości sformatowaną etykietę z nazwą i gramaturą posiłku
            values.append(
                f"{meal.meal_name} ({meal.grams} g) - {meal.calories} kcal P: {meal.protein} F: {meal.fat} C: {meal.carbs}")
            print(values)
        return values
