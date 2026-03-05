from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from contests.models import Contest, ProblemLink
from submissions.models import Submission
from scoring.models import Score


class Command(BaseCommand):
    help = 'Create sample data to demonstrate HackHub-Code workflow'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for HackHub-Code...\n')

        # Create users
        organizer, _ = User.objects.get_or_create(
            username='organizer1',
            defaults={'email': 'organizer@hackhub.com', 'role': 'organizer',
                      'first_name': 'Alice', 'last_name': 'Organizer'}
        )
        organizer.set_password('hackhub123')
        organizer.save()
        self.stdout.write(f'  [OK] Organizer: organizer1 / hackhub123')

        p1, _ = User.objects.get_or_create(
            username='participant1',
            defaults={'email': 'p1@hackhub.com', 'role': 'participant',
                      'first_name': 'Bob', 'last_name': 'Coder'}
        )
        p1.set_password('hackhub123')
        p1.save()

        p2, _ = User.objects.get_or_create(
            username='participant2',
            defaults={'email': 'p2@hackhub.com', 'role': 'participant',
                      'first_name': 'Carol', 'last_name': 'Dev'}
        )
        p2.set_password('hackhub123')
        p2.save()
        self.stdout.write(f'  [OK] Participants: participant1, participant2 / hackhub123')

        judge, _ = User.objects.get_or_create(
            username='judge1',
            defaults={'email': 'judge@hackhub.com', 'role': 'judge',
                      'first_name': 'Dave', 'last_name': 'Evaluator'}
        )
        judge.set_password('hackhub123')
        judge.save()

        judge2, _ = User.objects.get_or_create(
            username='judge2',
            defaults={'email': 'judge2@hackhub.com', 'role': 'judge',
                      'first_name': 'Eve', 'last_name': 'Reviewer'}
        )
        judge2.set_password('hackhub123')
        judge2.save()
        self.stdout.write(f'  [OK] Judges: judge1, judge2 / hackhub123')

        # Create admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hackhub.com', 'admin123', role='organizer')
            self.stdout.write(f'  [OK] Admin: admin / admin123')

        now = timezone.now()

        # Contest 1: Active (running now)
        c1, _ = Contest.objects.get_or_create(
            title='HackHub Spring Contest 2025',
            defaults={
                'description': 'The premier coding challenge of the season! Solve algorithmic problems and showcase your coding skills. This is a general-purpose contest open to all skill levels.',
                'rules': '1. One submission per participant.\n2. Submit before the deadline.\n3. Solutions must be your own work.\n4. ZIP files must be under 10MB.\n5. External links must be accessible.',
                'start_time': now - timedelta(hours=2),
                'end_time': now + timedelta(hours=22),
                'created_by': organizer,
                'is_published': True,
            }
        )
        ProblemLink.objects.get_or_create(contest=c1, title='Two Sum', defaults={'url': 'https://leetcode.com/problems/two-sum/', 'platform': 'leetcode'})
        ProblemLink.objects.get_or_create(contest=c1, title='Fibonacci Series', defaults={'url': 'https://www.hackerrank.com/challenges/fibonacci-modified/problem', 'platform': 'hackerrank'})
        ProblemLink.objects.get_or_create(contest=c1, title='Graph DFS', defaults={'url': 'https://codeforces.com/problemset/problem/104/B', 'platform': 'codeforces'})
        self.stdout.write(f'  [OK] Active Contest: "{c1.title}"')

        # Contest 2: Upcoming
        c2, _ = Contest.objects.get_or_create(
            title='HackHub Summer Hackathon',
            defaults={
                'description': 'A 24-hour hackathon where you build and submit creative solutions to real-world problems.',
                'rules': '1. Teams of up to 3.\n2. Use any programming language.\n3. Submit a working solution link.',
                'start_time': now + timedelta(days=3),
                'end_time': now + timedelta(days=4),
                'created_by': organizer,
                'is_published': True,
            }
        )
        ProblemLink.objects.get_or_create(contest=c2, title='Build a REST API', defaults={'url': 'https://github.com/explore', 'platform': 'other'})
        self.stdout.write(f'  [OK] Upcoming Contest: "{c2.title}"')

        # Contest 3: Ended (with submissions and scores)
        c3, _ = Contest.objects.get_or_create(
            title='HackHub Winter Challenge',
            defaults={
                'description': 'Archived contest with full data for leaderboard exploration.',
                'rules': '1. Individual submissions only.\n2. ZIP or GitHub links accepted.',
                'start_time': now - timedelta(days=10),
                'end_time': now - timedelta(days=3),
                'created_by': organizer,
                'is_published': True,
            }
        )
        ProblemLink.objects.get_or_create(contest=c3, title='Matrix Rotation', defaults={'url': 'https://www.hackerrank.com/challenges/matrix-rotation-algo/problem', 'platform': 'hackerrank'})
        self.stdout.write(f'  [OK] Ended Contest: "{c3.title}"')

        # Submissions for past contest
        sub1, _ = Submission.objects.get_or_create(
            contest=c3, participant=p1,
            defaults={'submission_type': 'github', 'external_link': 'https://github.com/participant1/winter-solution'}
        )
        sub2, _ = Submission.objects.get_or_create(
            contest=c3, participant=p2,
            defaults={'submission_type': 'leetcode', 'external_link': 'https://leetcode.com/problems/two-sum/submissions/'}
        )
        self.stdout.write(f'  [OK] Added submissions for past contest')

        # Scores
        Score.objects.get_or_create(submission=sub1, judge=judge, defaults={'score': 88.5, 'feedback': 'Excellent approach. Clean code, well-documented. Minor optimization could improve runtime.'})
        Score.objects.get_or_create(submission=sub1, judge=judge2, defaults={'score': 91.0, 'feedback': 'Impressive solution. Edge cases handled well.'})
        Score.objects.get_or_create(submission=sub2, judge=judge, defaults={'score': 74.0, 'feedback': 'Good attempt. Some edge cases missed. Code could be cleaner.'})
        Score.objects.get_or_create(submission=sub2, judge=judge2, defaults={'score': 77.5, 'feedback': 'Decent solution, but efficiency could be improved.'})
        self.stdout.write(f'  [OK] Added scores - leaderboard ready for "{c3.title}"')

        self.stdout.write('\nSample data created successfully!\n')
        self.stdout.write('All user passwords: hackhub123 (admin: admin123)\n')
        self.stdout.write('Accounts:\n')
        self.stdout.write('   organizer1 -> Organizer role\n')
        self.stdout.write('   participant1, participant2 -> Participant role\n')
        self.stdout.write('   judge1, judge2 -> Judge role\n')
        self.stdout.write('   admin -> Superuser\n')
        self.stdout.write('\nRun: python manage.py runserver\n')
