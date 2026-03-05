from django.urls import path
from . import views

# the main navigation and contest discovery paths
urlpatterns = [
    # homepage and deep dive into a single contest
    path('', views.ContestListView.as_view(), name='homepage'),
    path('contests/<int:pk>/', views.ContestDetailView.as_view(), name='contest_detail'),
    
    # organizer tools for building and managing their events
    path('contests/create/', views.create_contest, name='create_contest'),
    path('contests/<int:pk>/edit/', views.edit_contest, name='edit_contest'),
    path('contests/<int:pk>/publish/', views.publish_contest, name='publish_contest'),
    path('contests/my/', views.MyContestsView.as_view(), name='my_contests'),
    path('contests/<int:pk>/delete/', views.delete_contest, name='delete_contest'),
    
    # results, searching, and general platform info
    path('contests/<int:pk>/leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
