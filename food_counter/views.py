from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Meal, Date, Products, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import DateForm, MealForm, ProductsSearchForm, DateCreateForm
from .forms import MealSearchForm

class DateListView(LoginRequiredMixin, ListView):
    model = Date
    template_name = 'food_counter/home.html'
    context_object_name = 'dates'
    paginate_by = 9

    def get_queryset(self):
        return Date.objects.filter(user=self.request.user).order_by('-date')


class DateDetailView(LoginRequiredMixin, DetailView):
    model = Date


class DateCreateView(LoginRequiredMixin, CreateView):
    model = Date
    form_class = DateCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            # Dodaj komunikat za pomocą messages.error
            messages.error(self.request, 'Date needs to be unique & correct')
            return self.render_to_response(self.get_context_data(form=form))


class DateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Date
    form_class = DateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.save()  # To update calories and macros
        return super().form_valid(form)

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    success_url = "/"
    form_class = MealForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)


class MealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meal
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
    model = Products
    fields = ["product_name", "calories", "protein", "fat", "carbs", "category"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


#  IT IS NOT USED - NEEDS EVALUATION IF NEEDED - also test function
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    fields = ["product_name", "calories", "protein", "fat", "carbs", "category"]
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)


class MealListView(ListView):
    model = Meal
    template_name = 'food_counter/meal_list.html'
    context_object_name = 'meals'
    # paginate_by = 30 - Other way is needed to paginate by category
    ordering = ['meal_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MealSearchForm(self.request.GET)
        context['categories'] = Category.objects.all().order_by('name')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = MealSearchForm(self.request.GET)
        if form.is_valid():
            meal_name = form.cleaned_data['meal_name']
            if meal_name:  # if meal_name not empty then search by name
                queryset = queryset.filter(meal_name__icontains=meal_name)

        queryset = queryset.filter(user=self.request.user)
        return queryset


class ProductsListView(ListView):
    model = Products
    template_name = 'food_counter/products_list.html'
    context_object_name = 'products'
    # paginate_by = 30 - Other way is needed to paginate by category
    ordering = ['-product_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductsSearchForm(self.request.GET)
        context['categories'] = Category.objects.all().order_by('name')
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

    def test_func(self):
        meal = self.get_object()
        if meal.user is not None:
            if self.request.user == meal.user:
                return True
        return False


class DateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Date
    success_url = '/'
    template_name = "food_counter/date_confirm_delete.html"

    def test_func(self):
        date = self.get_object()
        if self.request.user == date.user:
            return True
        return False


def about(request):
    return render(request, 'food_counter/about.html')
