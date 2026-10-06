from django.urls import path
from . import views
urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("task/new/", views.task_edit, name="task_new"),
    path("task/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("task/<int:pk>/toggle/", views.task_toggle, name="task_toggle"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("category/add/", views.category_add, name="category_add"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
]
