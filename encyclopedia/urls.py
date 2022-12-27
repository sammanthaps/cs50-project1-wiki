from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="homepage"),
    path(r"wiki/<str:value>/", views.entry, name="entry"),
    path("wiki/search", views.search_form, name="search"),
    path("wiki/new_page", views.new_page, name="newPage"),
    path(r"wiki/<str:value>/editing_page", views.edit_form, name="editPage"),
    path("wiki/random", views.random_page, name="random")
]
