from django.urls import path
from .views import home, reviews, save_review

urlpatterns = [
    path("", home),
    path("reviews/", reviews),
    path("save-review/", save_review),
]