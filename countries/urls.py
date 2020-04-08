from django.urls import path

from . import views


urlpatterns = [
    path('', views.countries_list, name='countries_list'),
    path('country/<str:country>/', views.country_cases, name='cases'),
]
