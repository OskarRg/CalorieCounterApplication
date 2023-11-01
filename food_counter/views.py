from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meal, Date, Products, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import DateForm, MealForm, ProductsSearchForm
from .forms import MealSearchForm


# Create your views here.
def home(request):
    context = {
        'meals': Meal.objects.all()
    }
    context = {
        'dates': Date.objects.filter(user=request.user)
    }
    print("CONTEXT: ", context)
    return render(request, 'food_counter/home.html', context)


class DateListView(ListView):
    model = Date
    template_name = 'food_counter/home.html'
    context_object_name = 'dates'
    paginate_by = 9

    def get_queryset(self):
        return Date.objects.filter(user=self.request.user).order_by('-date')

    # ordering = ['-date']


class DateDetailView(DetailView):
    model = Date


class DateCreateView(LoginRequiredMixin, CreateView):
    model = Date
    fields = ["date"]  # pola, które chcemy wypełnić w formularzu

    def form_valid(self, form):
        form.instance.user = self.request.user
        """
        # metoda, która jest wywoływana po walidacji formularza
        self.object = form.save(commit=False)  # zapisujemy obiekt Date z danymi z formularza, ale nie zapisujemy go jeszcze w bazie danych
        self.object.user = self.request.user  # przypisujemy wartość request.user do pola user obiektu Date
        self.object.save()  # zapisujemy obiekt Date w bazie danych
        """
        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP


'''
class DateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Date
    fields = ["date", "meals"]  # pola, które chcemy wypełnić w formularzu

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False
'''


class DateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Date  # model, który chcemy zaktualizować
    form_class = DateForm  # klasa formularza, która definiuje pole meals

    # success_url = "/"  # url, na który chcemy przekierować po zaktualizowaniu obiektu

    def get_form_kwargs(self):
        # Metoda, która zwraca argumenty do konstruktora formularza
        kwargs = super().get_form_kwargs()
        # Dodajemy użytkownika jako argument
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        # metoda, która jest wywoływana po walidacji formularza
        self.object = form.save()  # zapisujemy obiekt Date z danymi z formularza
        self.object.save()  # wywołujemy ponownie metodę save(), aby zaktualizować wartości kalorii i makroskładników na podstawie posiłków
        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal  # model, który chcemy utworzyć
    # fields = ["meal_name", "products", "category", "grams"]
    success_url = "/"
    form_class = MealForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()  # zapisujemy obiekt Date z danymi z formularza
        self.object.save()  # wywołujemy ponownie metodę save(), aby zaktualizować wartości kalorii i makroskładników na podstawie posiłków
        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meal  # model, który chcemy utworzyć
    #  fields = ["meal_name", "category", "grams"]
    success_url = "/"
    form_class = MealForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        meal = self.get_object()
        if meal.user is not None:
            if self.request.user == meal.user:
                return True
        return False


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products  # model, który chcemy utworzyć
    fields = ["product_name", "calories", "protein", "fat", "carbs", "category"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products  # model, który chcemy utworzyć
    fields = ["product_name", "calories", "protein", "fat", "carbs", "category"]
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)



#  Poniżej jest inna wersja z formularzem
'''
class MealListView(ListView):
    model = Meal
    template_name = 'food_counter/meal_list.html'
    context_object_name = 'meals'
    Meal.objects.all()
    # ordering = ['-date']
'''



class MealListView(ListView):
    model = Meal
    template_name = 'food_counter/meal_list.html'
    context_object_name = 'meals'
    paginate_by = 30
    ordering = ['meal_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MealSearchForm(self.request.GET)
        context['categories'] = Category.objects.all().order_by('name')  # Dodaj dostęp do kategorii
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = MealSearchForm(self.request.GET)  # Seach form
        if form.is_valid():
            meal_name = form.cleaned_data['meal_name']
            if meal_name:  # meal_name not empty
                queryset = queryset.filter(meal_name__icontains=meal_name)

        queryset = queryset.filter(user=self.request.user)
        return queryset


class ProductsListView(ListView):
    model = Products
    template_name = 'food_counter/products_list.html'
    context_object_name = 'products'
    # paginate_by = 30
    ordering = ['-product_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductsSearchForm(self.request.GET)

        # Pobierz wszystkie kategorie
        all_categories = Category.objects.all().order_by('name')
        context['categories'] = all_categories
        print("CONTEXT ___________________")
        print(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProductsSearchForm(self.request.GET)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            if product_name:
                queryset = queryset.filter(product_name__icontains=product_name).order_by('category', 'product_name')

        return queryset.order_by('category__name')


class MealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meal
    success_url = '/meal/list/'

    # context_object_name = 'meals'

    def test_func(self):
        meal = self.get_object()
        if meal.user is not None:
            if self.request.user == meal.user:
                return True
        return False


class DateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Date
    success_url = '/'
    template_name = "food_counter/meal_confirm_delete.html"  # używamy innego szablonu html dla widoku

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False


def about(request):
    return render(request, 'food_counter/about.html')
