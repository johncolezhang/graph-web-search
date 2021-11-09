from django.urls import path
from . import views

urlpatterns = [
    path("add_label_info", views.add_label_info),
    path("get_label_info", views.get_label_info)
]