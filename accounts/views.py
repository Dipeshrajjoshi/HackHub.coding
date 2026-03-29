from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
import logging
from hackhub.exceptions import HackHubError, PermissionDeniedError
from django.db import DatabaseError

logger = logging.getLogger('django')


def register_view(request):
    # don't show the register page if they are already logged in
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user) # log them in automatically after they sign up
                messages.success(request, f'Welcome to HACKHUB-CODE, {user.username}!')
                return redirect('/')
            except DatabaseError as e:
                # catch DB issues separately like we do in Java
                logger.error(f"Registration Database Error: {e}", exc_info=True)
                messages.error(request, "A database error occurred during registration.")
            except Exception as e:
                # fallback for any other unexpected crashes
                logger.error(f"Unexpected Registration Error: {e}", exc_info=True)
                messages.error(request, "An unexpected error occurred.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # if they were trying to go somewhere specific, send them there
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    # standard logout, only works with POST for security
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('/accounts/login/')


from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # just shows the user's detailed info
    return render(request, 'accounts/profile.html', {'user': request.user})


def user_history_view(request):
    # pull stats and contest history from the session (the things we saved in the middleware/cookies)
    try:
        visit_stats = request.session.get('visit_stats', {})
        recent_contest_ids = request.session.get('recent_contests', [])
        
        from contests.models import Contest
        recent_contests = Contest.objects.filter(id__in=recent_contest_ids)
        # sorting them so they match the order we visited them (most recent first)
        recent_contests = sorted(recent_contests, key=lambda x: recent_contest_ids.index(x.id))
    except Exception as e:
        # if the session data is bad, just show an empty history instead of a 500 error
        logger.error(f"User History Error (User {request.user.id}): {e}", exc_info=True)
        visit_stats = {}
        recent_contests = []
    
    return render(request, 'accounts/user_history.html', {
        'visit_stats': visit_stats,
        'recent_contests': recent_contests,
    })
