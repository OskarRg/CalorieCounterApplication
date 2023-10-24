from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meal, Date
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import DateForm
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
    fields = ["meal_name", "calories", "protein", "fat", "carbs"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)  # wywołujemy metodę nadrzędną, która zwraca odpowiedź HTTP


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meal  # model, który chcemy utworzyć
    fields = ["meal_name", "calories", "protein", "fat", "carbs"]
    success_url = "/"

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

    ordering = ['meal_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MealSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = MealSearchForm(self.request.GET) # stwórz formularz tutaj
        if form.is_valid():
            meal_name = form.cleaned_data['meal_name']
            if meal_name:  # jeśli pole meal_name jest obecne i niepuste
                queryset = queryset.filter(meal_name__icontains=meal_name)  # filtruj queryset według pola meal_name

        return queryset

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
    template_name = "food_counter/meal_confirm_delete.html" # używamy innego szablonu html dla widoku

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False




def about(request):
    return render(request, 'food_counter/about.html')
