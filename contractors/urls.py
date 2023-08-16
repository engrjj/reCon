from django.urls import path
from contractors import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "contractors"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login_page'),
    path('login/process', views.login_process, name='login_process'),
    path('contractor/register', views.contractor_registration, name='contractor_register'),
    path('contractor/register/process', views.contractor_process, name='contractor_process'),
    path('contractor/profile/<int:contractor_id>', views.contractor_profile, name="contractor_profile"),
    path('contractor/profile/<int:contractor_id>/upload', views.upload_contractor_image, name="upload_contractor_image"),
    path('images/contractor/<int:image_id>/delete', views.delete_contractor_image, name="delete_contractor_image"),
    path('contractor/profile/<int:contractor_id>/edit', views.edit_profile, name="edit_profile"),
    path('contractor/profile/<int:contractor_id>/edit/process', views.edit_profile_process, name="edit_profile_process"),
    path('contractor/profile/<int:contractor_id>/remove_logo', views.delete_contractor_logo, name="delete_contractor_logo"),
    path('contractor/dashboard', views.contractor_dashboard, name='contractor_dashboard'),
    path('contractor/projects/create', views.create_project, name="create_project"),
    path('contractor/projects/create/process', views.create_process, name="create_process"),
    path('contractor/projects/<int:project_id>', views.show_project, name="show_project"),
    path('contractor/projects/<int:project_id>/upload', views.upload_project_image, name="upload_project_image"),
    path('images/<int:image_id>/delete', views.delete_image, name="delete_project_image"),
    path('contractor/projects/<int:project_id>/edit', views.edit_project, name="edit_project"),
    path('contractor/projects/<int:project_id>/edit/process', views.edit_process, name="edit_process"),
    path('contractor/projects/<int:project_id>/createUpdate', views.create_update, name="create_update"),
    path('contractor/projects/<int:project_id>/createUpdate/process', views.update_process, name="update_process"),
    path('contractor/projects/<int:project_id>/updates/<int:update_id>', views.show_update, name="show_update"),
    path('contractor/projects/<int:project_id>/updates/<int:update_id>/upload', views.upload_update_image, name="upload_update_image"),
    path('images/updates/<int:image_id>/delete', views.delete_update_image, name="delete_update_image"),
    path('contractor/projects/<int:project_id>/updates/<int:update_id>/edit', views.edit_update, name="edit_update"),
    path('contractor/projects/<int:project_id>/updates/<int:update_id>/edit/process', views.edit_update_process, name="edit_update_process"),
    path('contractor/projects/<int:project_id>/updates/<int:update_id>/delete', views.delete_update, name="delete_update"),
    path('contractor/projects/<int:project_id>/delete', views.delete_project, name="delete_project"),
    path('logout', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)