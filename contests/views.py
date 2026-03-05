from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Q
from .models import Contest, ProblemLink
from .forms import ContestForm, ProblemLinkFormSet
from submissions.models import Submission
from scoring.models import Score
import logging
from hackhub.exceptions import ContestError, PermissionDeniedError
from django.db import DatabaseError

logger = logging.getLogger('django')


from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# using a class-based view to list all the published contests on the home page
class ContestListView(ListView):
    model = Contest
    template_name = 'contests/homepage.html'
    context_object_name = 'contests'
    # we only want to show contests that are actually live
    queryset = Contest.objects.filter(is_published=True).order_by('-start_time')


# shows the details of a single contest like rules and problem links
class ContestDetailView(DetailView):
    model = Contest
    template_name = 'contests/contest_detail.html'
    context_object_name = 'contest'

    def get_queryset(self):
        # if logged in, let the creator see their own drafts too
        if self.request.user.is_authenticated:
            return Contest.objects.filter(Q(is_published=True) | Q(created_by=self.request.user))
        return Contest.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        try:
            # keeping track of what contests the user looked at using sessions
            recent_contests = request.session.get('recent_contests', [])
            contest_id = self.object.id
            if contest_id in recent_contests:
                recent_contests.remove(contest_id)
            recent_contests.insert(0, contest_id)
            request.session['recent_contests'] = recent_contests[:5] # only save the last 5
            
            # counting how many times they visited today
            today = timezone.now().date().isoformat()
            visit_stats = request.session.get('visit_stats', {})
            visit_stats[today] = visit_stats.get(today, 0) + 1
            request.session['visit_stats'] = visit_stats
            
            # also dropping a cookie just to remember the date they last visited
            response.set_cookie('last_visit', today, max_age=86400) # expires in 24 hours
        except (KeyError, TypeError) as e:
            # if session data is weird, just log a warning and don't crash the page
            logger.warning(f"Session data corrupted for user {request.user.id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in history tracking for contest {self.object.id}: {e}", exc_info=True)
        finally:
            # this runs no matter what, just like in java
            pass
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # adding the problems and checking if the user already submitted something
        context['problem_links'] = self.object.problem_links.all()
        context['now'] = timezone.now()
        
        if self.request.user.is_authenticated and self.request.user.is_participant():
            context['user_submission'] = Submission.objects.filter(
                contest=self.object, participant=self.request.user
            ).first()
        return context


# handle searching for contests by name or description
class SearchView(ListView):
    model = Contest
    template_name = 'contests/search_results.html'
    context_object_name = 'contests'

    def get_queryset(self):
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        object_list = Contest.objects.filter(is_published=True)
        
        # filter by keyword if the user typed something
        if query:
            object_list = object_list.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        
        # for status, we have to check the model method so we use a list comprehension
        if status:
            object_list = [c for c in object_list if c.status() == status]
            
        return object_list


def about_view(request):
    return render(request, 'contests/about.html')


from .forms import ContestForm, ProblemLinkFormSet, ContactForm

# handle the contact us form and save a copy to a text file
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            # writing to a file just to show we can handle file IO
            try:
                with open('contact_messages.txt', 'a') as f:
                    f.write(f"--- Message from {contact_msg.name} ({contact_msg.email}) ---\n")
                    f.write(f"Date: {contact_msg.created_at}\n")
                    f.write(f"Message: {contact_msg.message}\n")
                    f.write("-" * 40 + "\n\n")
            except Exception as e:
                print(f"Error writing to contact_messages.txt: {e}")
                
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contests/contact.html', {'form': form})


@login_required
def create_contest(request):
    # security check: only let organizers build new contests
    if not request.user.is_organizer():
        messages.error(request, 'Only organizers can create contests.')
        return redirect('/')
        
    if request.method == 'POST':
        form = ContestForm(request.POST)
        formset = ProblemLinkFormSet(request.POST) # handling the problem links at the same time
        if form.is_valid() and formset.is_valid():
            contest = form.save(commit=False)
            contest.created_by = request.user
            contest.save()
            formset.instance = contest
            formset.save()
            messages.success(request, 'Contest created successfully!')
            return redirect('contest_detail', pk=contest.pk)
    else:
        form = ContestForm()
        formset = ProblemLinkFormSet()
    return render(request, 'contests/create_contest.html', {'form': form, 'formset': formset})


@login_required
def edit_contest(request, pk):
    # make sure the person editing actually owns the contest
    contest = get_object_or_404(Contest, pk=pk, created_by=request.user)
    if not request.user.is_organizer():
        messages.error(request, 'Permission denied.')
        return redirect('/')
    # don't allow edits after it's finished
    if contest.is_expired():
        messages.error(request, "You cannot edit a contest that has ended.")
        return redirect('contest_detail', pk=pk)
        
    if request.method == 'POST':
        form = ContestForm(request.POST, instance=contest)
        formset = ProblemLinkFormSet(request.POST, instance=contest)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Contest updated successfully!')
            return redirect('contest_detail', pk=contest.pk)
    else:
        form = ContestForm(instance=contest)
        formset = ProblemLinkFormSet(instance=contest)
    return render(request, 'contests/edit_contest.html', {'form': form, 'formset': formset, 'contest': contest})


@login_required
def publish_contest(request, pk):
    contest = get_object_or_404(Contest, pk=pk, created_by=request.user)
    try:
        # custom error handling pattern (like Java try-catch blocks)
        if not request.user.is_organizer():
            raise PermissionDeniedError("Only organizers can publish contests.")
        
        contest.is_published = True
        contest.save()
        messages.success(request, f'"{contest.title}" is now published!')
    except PermissionDeniedError as e:
        messages.error(request, str(e))
        return redirect('/')
    except DatabaseError as e:
        # specific catch for DB issues, logging the detailed error
        logger.error(f"Database error publishing contest {pk}: {e}", exc_info=True)
        messages.error(request, "A database error occurred. Please try again later.")
    except Exception as e:
        # catch-all for any other weird stuff
        logger.error(f"Unexpected error publishing contest {pk}: {e}", exc_info=True)
        messages.error(request, "An unexpected error occurred.")
    return redirect('contest_detail', pk=pk)


@login_required
def delete_contest(request, pk):
    # only the creator can delete their own contest
    contest = get_object_or_404(Contest, pk=pk, created_by=request.user)
    
    if not request.user.is_organizer():
         messages.error(request, 'Permission denied.')
         return redirect('/')

    if request.method == 'POST':
        title = contest.title
        contest.delete()
        messages.success(request, f'Contest "{title}" has been deleted.')
        return redirect('my_contests')
    
    return render(request, 'contests/delete_contest.html', {'contest': contest})


# view for organizers to see their own list of work
class MyContestsView(LoginRequiredMixin, ListView):
    model = Contest
    template_name = 'contests/my_contests.html'
    context_object_name = 'contests'

    def get_queryset(self):
        if not self.request.user.is_organizer():
            return Contest.objects.none()
        return Contest.objects.filter(created_by=self.request.user).order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        # extra security check before running the view
        if not request.user.is_authenticated or not request.user.is_organizer():
            messages.error(request, 'Permission denied.')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


# showing the rankings for a specific contest
class LeaderboardView(DetailView):
    model = Contest
    template_name = 'contests/leaderboard.html'
    context_object_name = 'contest'

    def get_queryset(self):
        return Contest.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contest = self.object
        
        # getting all submissions and calculating the average scores for ranking
        submissions = Submission.objects.filter(contest=contest).annotate(
            avg_score=Avg('scores__score'),
            score_count=Count('scores')
        ).select_related('participant').order_by('-avg_score')
        
        leaderboard_data = []
        for i, submission in enumerate(submissions):
            leaderboard_data.append({
                'submission': submission,
                'avg_score': round(submission.avg_score, 2) if submission.avg_score is not None else None,
                'score_count': submission.score_count,
                'rank': i + 1,
            })
        
        context['leaderboard_data'] = leaderboard_data
        return context

    def get(self, request, *args, **kwargs):
        # tracking leaderboard hits too
        response = super().get(request, *args, **kwargs)
        pk = self.kwargs.get('pk')
        recent_contests = request.session.get('recent_contests', [])
        if pk in recent_contests:
            recent_contests.remove(pk)
        recent_contests.insert(0, pk)
        request.session['recent_contests'] = recent_contests[:5]
        return response
