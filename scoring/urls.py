from django.urls import path
from . import views

# judge-specific tools for evaluating student work
urlpatterns = [
    # main entry for judges to see all contests
    path('dashboard/', views.judge_dashboard, name='judge_dashboard'),
    
    # drill down into all student submissions for a specific contest
    path('contest/<int:contest_pk>/submissions/', views.judge_contest_submissions, name='judge_contest_submissions'),
    
    # the actual marking/evaluation form for a single submission
    path('score/<int:submission_pk>/', views.score_submission, name='score_submission'),
]
