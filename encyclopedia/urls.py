from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("randomPage", views.randomPage, name="random"),
    path("searchResults", views.searchResults, name="results"),
    path("savePage", views.savePage, name="savepage"),
    path("newPage", views.createNewPage, name="newpage"),
    path("<slug:title>/saveEdits", views.saveEdits, name="save_edits"),
    path("wiki/<slug:title>", views.entryPage, name="entrypage"),
    path("<slug:title>/editPage", views.editPage, name="editpage"),
    path("<slug:title>/deletePage", views.deletePage, name="deletepage"),
]
