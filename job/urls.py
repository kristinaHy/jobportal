from django.contrib import admin
from django.urls import path, include
from job_app import urls as job_app_urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from job_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('post/', views.JobCreateView.as_view(), name='post_job'),
    path('apply/<int:pk>/', views.ApplyJobView.as_view(), name='apply_job'),
    path('update/<int:pk>/', views.JobUpdateView.as_view(), name='update_job'),
    path('delete/<int:pk>/', views.JobDeleteView.as_view(), name='delete_job'),
    path('job/<int:pk>/applicants/', views.ApplicantsListView.as_view(), name='applicants_list'),
    path('application/<int:pk>/', views.ViewApplicantView.as_view(), name='view_applicant'),
    path('application/<int:pk>/update-status/', views.update_application_status, name='update_application_status'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(job_app_urls)),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
