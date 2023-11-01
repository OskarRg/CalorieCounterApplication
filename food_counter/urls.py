from django.contrib import admin
from .views import (DateListView, DateDetailView,
                    DateCreateView, DateUpdateView, MealCreateView, DateDeleteView,
                    MealListView, MealUpdateView, MealDeleteView ,ProductCreateView, ProductUpdateView, ProductsListView
                    )

from django.urls import path
from . import views

urlpatterns = [
    path('', DateListView.as_view(), name='food_counter-home'),
    path('date/<int:pk>/', DateDetailView.as_view(), name='date-detail'),
    path('date/<int:pk>/update/', DateUpdateView.as_view(), name='date-update'),
    path('date/<int:pk>/delete/', DateDeleteView.as_view(), name='date-delete'),
    path('date/new/', DateCreateView.as_view(), name='date-create'),
    path('meal/new/', MealCreateView.as_view(), name='meal-create'),
    path('meal/<int:pk>/update/', MealUpdateView.as_view(), name='meal-update'),
    path('meal/<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),
    path('meal/list/', MealListView.as_view(), name='meal-list'),
    path('product/new/', ProductCreateView.as_view(), name='product-create'),
    path('product/list/', ProductsListView.as_view(), name='product-list'),
    path('about/', views.about, name='food_counter-about'),
]


