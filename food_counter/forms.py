from django import forms
from .models import Date, Meal, Products, Category


class DateCreateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ["date"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class DateForm(forms.ModelForm):
    meals = forms.ModelMultipleChoiceField(queryset=Meal.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Date
        fields = ["meals"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meals'].queryset = Meal.objects.filter(user=user).order_by('meal_name')
        self.fields['meals'].initial = [meal.id for meal in self.instance.meals.all()]


class MealForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Products.objects.all().order_by('product_name'), required=True, widget=forms.Select)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select)

    class Meta:
        model = Meal
        fields = ["meal_name", "product", 'grams', 'category']


class MealSearchForm(forms.ModelForm):
    meal_name = forms.CharField(max_length=100, required=False, label='')

    class Meta:
        model = Meal
        fields = ['meal_name']


class ProductsSearchForm(forms.ModelForm):
    product_name = forms.CharField(max_length=100, required=False, label='')

    class Meta:
        model = Products
        fields = ['product_name']
