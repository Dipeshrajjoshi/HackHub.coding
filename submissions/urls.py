from django.urls import path
from . import views

# paths for participants to upload their solutions
urlpatterns = [
    # submitting to a specific contest event
    path('contest/<int:contest_pk>/submit/', views.submit, name='submit'),
    
    # general upload tool
    path('upload/', views.upload_view, name='upload'),
    
    # confirmation page after a successful submission
    path('confirmation/<int:pk>/', views.submission_confirmation, name='submission_confirmation'),
]
