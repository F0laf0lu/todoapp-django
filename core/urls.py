from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='default-home'),
    path('<str:current_date>/', views.home, name="home" ),
    path('add_task/<str:current_date>/', views.add_task, name="add-task"),
    path('delete_task/<int:id>/<str:current_date>/', views.delete_task, name="delete-task"),
    path("mark_task/<int:id>/", views.mark_task, name="mark_task"),
]
