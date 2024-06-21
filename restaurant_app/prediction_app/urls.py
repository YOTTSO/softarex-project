from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("predict_revenue", views.predict_revenue, name="predict_revenue"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path('history', views.prediction_history, name='history'),
    path('logout', LogoutView.as_view(), name='logout'),
]
