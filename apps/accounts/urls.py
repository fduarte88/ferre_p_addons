from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:login'), name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
