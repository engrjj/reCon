from django.urls import path
from users import views

app_name = "users"
urlpatterns = [
    path('register', views.user_registration, name='user_register'),
    path('register/process', views.user_process, name='user_process'),
    path('dashboard', views.user_dashboard, name='user_dashboard'),
    path('add_project', views.add_project, name='user_add_project'),
    path('remove_project/<int:project_id>', views.remove_project, name="user_remove_project"),
    path('browse', views.contractor_list, name='contractors_list'),
    path('sort', views.sort, name='user_sort'),
]