from django.urls import path
from . import views

# grouping all the user-related paths together
urlpatterns = [
    # standard auth pages: join, sign-in, sign-out
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # user details and their past activity history
    path('profile/', views.profile_view, name='profile'),
    path('history/', views.user_history_view, name='user_history'),
]
