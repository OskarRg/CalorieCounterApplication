from django import forms
# from bootstrap_datepicker_plus.widgets import DatePickerInput
from food_counter.models import Date
from .widgets import MealCheckboxSelectMultiple # Importujemy nasz widget
from django import forms
from .models import Date, Meal, Products, Category


class DateForm(forms.ModelForm):
    # pole meals typu ModelChoiceField, które pozwala na wybór jednego posiłku z modelu Meal
    meals = forms.ModelMultipleChoiceField(queryset=Meal.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Date  # model, który chcemy zaktualizować
        fields = ["meals"]  # pole, które chcemy zmienić w formularzu

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ustawiamy queryset meals na posiłki należące do użytkownika i sortujemy je według nazwy rosnąco i kategorii malejąco
        self.fields['meals'].queryset = Meal.objects.filter(user=user).order_by('category', 'meal_name')
        self.fields['meals'].initial = [meal.id for meal in self.instance.meals.all()]


class MealForm(forms.ModelForm):
    # pole meals typu ModelMultipleChoiceField, które pozwala na wybór wielu posiłków z modelu Meal
    # meals = forms.ModelMultipleChoiceField(queryset=Meal.objects.all())

    products = forms.ModelMultipleChoiceField(queryset=Products.objects.all().order_by('product_name'), required=False, widget=forms.CheckboxSelectMultiple)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select)

    class Meta:
        model = Meal  # model, który chcemy zaktualizować
        fields = ["meal_name", "products", 'grams', 'category']  # pole, które chcemy zmienić w formularzu


class MealSearchForm(forms.ModelForm):
    meal_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Meal
        fields = ['meal_name']


class ProductsSearchForm(forms.ModelForm):
    product_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Products
        fields = ['product_name']



"""
class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ["date"]
        widgets = {
            "date": DatePickerInput()
        }"""
