from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# the main URL routing for the whole HackHub platform
urlpatterns = [
    # standard django admin area
    path('admin/', admin.site.urls),
    
    # account management: login, signup, and profile
    path('accounts/', include('accounts.urls')),
    
    # built-in django auth for password resets, etc.
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # file submissions and participant tools
    path('submissions/', include('submissions.urls')),
    
    # judge dashboard and scoring tools
    path('judge/', include('scoring.urls')),
    
    # everything else (homepage, contests, search, leaderboard)
    path('', include('contests.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # serving uploaded files locally

# custom error pages for 404 (not found) and 500 (server crash)
handler404 = 'hackhub.views.error_404'
handler500 = 'hackhub.views.error_500'
handler403 = 'hackhub.views.error_403'
