from django import forms
# from bootstrap_datepicker_plus.widgets import DatePickerInput
from food_counter.models import Date

from django import forms
from .models import Date, Meal


class DateForm(forms.ModelForm):
    # pole meals typu ModelMultipleChoiceField, które pozwala na wybór wielu posiłków z modelu Meal
    # meals = forms.ModelMultipleChoiceField(queryset=Meal.objects.all())

    meals = forms.ModelMultipleChoiceField(queryset=Meal.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Date  # model, który chcemy zaktualizować
        fields = ["meals"]  # pole, które chcemy zmienić w formularzu


class MealSearchForm(forms.ModelForm):
    meal_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Meal
        fields = ['meal_name']


"""
class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ["date"]
        widgets = {
            "date": DatePickerInput()
        }"""
