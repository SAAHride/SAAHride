from django.urls import path
from . import views

urlpatterns = [
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/accept/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('driver/start/<int:ride_id>/', views.start_ride, name='start_ride'),        # ✅ NEW
    path('driver/complete/<int:ride_id>/', views.complete_ride, name='complete_ride'),# ✅ NEW
    path('request-ride/', views.request_ride_view, name='request_ride'),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('driver/register/', views.driver_register_view, name='driver_register'),
]