from django.urls import path
from .views import profile, edit_profile

from .views import (
    JobListView, JobDetailView, JobCreateView, 
    ApplyJobView, JobUpdateView, JobDeleteView,
    ApplicantsListView, ViewApplicantView,
    signup, update_application_status
)




urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    path('', JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('post/', JobCreateView.as_view(), name='post_job'),
    path('apply/<int:pk>/', ApplyJobView.as_view(), name='apply_job'),
    path('update/<int:pk>/', JobUpdateView.as_view(), name='update_job'),
    path('delete/<int:pk>/', JobDeleteView.as_view(), name='delete_job'),
    path('job/<int:pk>/applicants/', ApplicantsListView.as_view(), name='applicants_list'),
    path('application/<int:pk>/', ViewApplicantView.as_view(), name='view_applicant'),
    path('application/<int:pk>/update-status/', update_application_status, name='update_application_status'),
    path('signup/', signup, name='signup'),

]
