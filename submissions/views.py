from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from contests.models import Contest
from .models import Submission
from .forms import SubmissionForm
import logging
from hackhub.exceptions import SubmissionError
from django.db import DatabaseError

logger = logging.getLogger('django')


@login_required
def submit(request, contest_pk):
    # participants only! judges and organizers shouldn't be submitting solutions
    if not request.user.is_participant():
        messages.error(request, 'Only participants can submit solutions.')
        return redirect('contest_detail', pk=contest_pk)

    contest = get_object_or_404(Contest, pk=contest_pk, is_published=True)

    # checking the clock to make sure the contest is still running
    if not contest.is_active():
        if contest.is_expired():
            messages.error(request, 'This contest has ended. Submissions are closed.')
        else:
            messages.error(request, 'This contest has not started yet.')
        return redirect('contest_detail', pk=contest_pk)

    # only one chance to submit per contest to keep it fair
    existing = Submission.objects.filter(contest=contest, participant=request.user).first()
    if existing:
        messages.warning(request, 'You have already submitted for this contest.')
        return redirect('submission_confirmation', pk=existing.pk)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                submission = form.save(commit=False)
                submission.contest = contest
                submission.participant = request.user
                if not submission.title:
                    submission.title = f"Submission for {contest.title}"
                submission.save()
                messages.success(request, 'Your solution has been submitted successfully!')
                return redirect('submission_confirmation', pk=submission.pk)
            except DatabaseError as e:
                # catch DB issues separately like we do in Java
                logger.error(f"Database Error for submission in contest {contest_pk}: {e}", exc_info=True)
                messages.error(request, "A database error occurred while saving your submission.")
            except Exception as e:
                # final catch-all for any other crashes
                logger.error(f"Unexpected Submission Error (Contest {contest_pk}, User {request.user.id}): {e}", exc_info=True)
                messages.error(request, "An unexpected error occurred. Please try again.")
                return render(request, 'submissions/submit.html', {'form': form, 'contest': contest})
    else:
        form = SubmissionForm(initial={'contest': contest})

    return render(request, 'submissions/submit.html', {
        'form': form,
        'contest': contest,
    })


@login_required
def upload_view(request):
    # similar logic to submit but purely for the generic upload page
    if not request.user.is_participant():
        messages.error(request, 'Only participants can upload files.')
        return redirect('/')

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            contest = form.cleaned_data.get('contest')
            
            # double check if the contest is actually okay to submit to
            if not contest.is_published or not contest.is_active():
                messages.error(request, 'You cannot submit to this contest at this time.')
                return render(request, 'submissions/upload.html', {'form': form})
            
            # prevent double submissions from this view too
            if Submission.objects.filter(contest=contest, participant=request.user).exists():
                messages.warning(request, f'You have already submitted for "{contest.title}".')
                return redirect('user_history')

            try:
                submission = form.save(commit=False)
                submission.participant = request.user
                submission.save()
                messages.success(request, 'File uploaded successfully!')
                return redirect('submission_confirmation', pk=submission.pk)
            except (DatabaseError, OSError) as e:
                # catching OS errors too, since we are dealing with files
                logger.error(f"Persistence/File Error (User {request.user.id}): {e}", exc_info=True)
                messages.error(request, "A system error occurred while saving your file.")
            except Exception as e:
                logger.error(f"Unexpected Upload Error (User {request.user.id}): {e}", exc_info=True)
                messages.error(request, "An unexpected error occurred.")
                return render(request, 'submissions/upload.html', {'form': form})
    else:
        form = SubmissionForm()
    
    return render(request, 'submissions/upload.html', {'form': form})


@login_required
def submission_confirmation(request, pk):
    # just a simple thank you page with the submission details
    submission = get_object_or_404(Submission, pk=pk, participant=request.user)
    return render(request, 'submissions/confirmation.html', {'submission': submission})
