from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Exists, OuterRef
from contests.models import Contest
from submissions.models import Submission
from scoring.models import Score
from .forms import ScoreForm
import logging
from hackhub.exceptions import ScoringError, PermissionDeniedError
from django.db import DatabaseError

logger = logging.getLogger('django')


@login_required
def judge_dashboard(request):
    # simple security check: judges only!
    if not request.user.is_judge():
        messages.error(request, 'Only judges can access this dashboard.')
        return redirect('/')
    # listing contests that have already ended so judges can start scoring
    contests = Contest.objects.filter(is_published=True).order_by('-end_time')
    return render(request, 'scoring/judge_dashboard.html', {'contests': contests})


@login_required
def judge_contest_submissions(request, contest_pk):
    if not request.user.is_judge():
        messages.error(request, 'Permission denied.')
        return redirect('/')
    contest = get_object_or_404(Contest, pk=contest_pk, is_published=True)
    
    # check if the judge already scored these submissions to show a checkmark in the UI
    judge_scores = Score.objects.filter(submission=OuterRef('pk'), judge=request.user)
    
    # using annotation to get the average score and count in one query (more efficient)
    submissions = Submission.objects.filter(contest=contest).annotate(
        avg_score=Avg('scores__score'),
        score_count=Count('scores'),
        already_scored=Exists(judge_scores)
    ).select_related('participant')
    
    submission_data = []
    for submission in submissions:
        submission_data.append({
            'submission': submission,
            'already_scored': submission.already_scored,
            'avg_score': round(submission.avg_score, 2) if submission.avg_score else None,
            'score_count': submission.score_count,
        })
    return render(request, 'scoring/contest_submissions.html', {
        'contest': contest,
        'submission_data': submission_data,
    })


@login_required
def score_submission(request, submission_pk):
    if not request.user.is_judge():
        messages.error(request, 'Only judges can score submissions.')
        return redirect('/')
        
    # security verify: contest must be officially published
    submission = get_object_or_404(Submission, pk=submission_pk, contest__is_published=True)
    
    # can't score while people are still working!
    if not submission.contest.is_expired():
        messages.error(request, 'You can only score submissions after the contest has ended.')
        return redirect('judge_contest_submissions', contest_pk=submission.contest.pk)
        
    existing_score = Score.objects.filter(submission=submission, judge=request.user).first()

    if request.method == 'POST':
        # if they already scored it, we update the existing record instead of making a new one
        if existing_score:
            form = ScoreForm(request.POST, instance=existing_score)
        else:
            form = ScoreForm(request.POST)
            
        try:
            # extra check during the POST just to be double safe
            if not request.user.is_judge():
                raise PermissionDeniedError("Only judges can score submissions.")
                
            score_obj = form.save(commit=False)
            score_obj.submission = submission
            score_obj.judge = request.user
            score_obj.save()
            messages.success(request, 'Score saved successfully!')
            return redirect('judge_contest_submissions', contest_pk=submission.contest.pk)
        except PermissionDeniedError as e:
            messages.error(request, str(e))
            return redirect('/')
        except DatabaseError as e:
            # log detailed DB error if something breaks during save
            logger.error(f"Database Error scoring submission {submission_pk}: {e}", exc_info=True)
            messages.error(request, "A database error occurred while saving the score.")
        except Exception as e:
            # general catch for any other issues
            logger.error(f"Score Error (Submission {submission_pk}, Judge {request.user.id}): {e}", exc_info=True)
            messages.error(request, f"Error saving score: {e}")
            return render(request, 'scoring/score_submission.html', {'form': form, 'submission': submission, 'existing_score': existing_score})
    else:
        form = ScoreForm(instance=existing_score)

    all_scores = Score.objects.filter(submission=submission)
    avg_score = all_scores.aggregate(Avg('score'))['score__avg']

    return render(request, 'scoring/score_submission.html', {
        'form': form,
        'submission': submission,
        'existing_score': existing_score,
        'all_scores': all_scores,
        'avg_score': round(avg_score, 2) if avg_score else None,
    })
