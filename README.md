# HackHub-Code

HackHub-Code is a platform we built to manage coding contests and hackathons. It's designed to be simple and focus on the actual work participants do, allowing judges to manually review and score submissions instead of just relying on automated tests.

---

### What does it do?

The main idea behind HackHub is to provide a place where organizers can set up contests, set deadlines, and let participants submit their solutions. We didn't include a heavy code execution engine on purpose—instead, we wanted something where judges can actually look at the code and the logic yourself.

- **Manage Timelines:** Set exactly when a contest starts and ends.
- **Flexible Submissions:** Support for all kinds of files (see below).
- **Manual Judging:** Judges can log in, view what's been submitted, and give a score from 0-100 with feedback.
- **Live Leaderboard:** Scores are averaged out across judges to show the final rankings.

---

### Supported Submission Formats

We tried to make the submission process as open as possible. For any contest, you can submit your work as:
- **ZIP Files:** Pack up your whole project and upload it directly.
- **External Links:** Links to GitHub repositories, hosted demos, or cloud folders.
- **Images:** Screenshots of your UI or diagrams (JPG/PNG).
- **Documents:** PDF or text files explaining your solution or design.

Since judges review everything manually, the platform is completely **language-agnostic**. You can submit anything from a Python script to a full-stack React app!

---

### Getting Started

If you want to run this locally, here's the quick version:

1.  **Install the basics:**
    ```bash
    pip install django django-crispy-forms crispy-bootstrap5 Pillow
    ```
2.  **Set up the database:**
    ```bash
    python manage.py migrate
    ```
3.  **Create some test data (optional):**
    ```bash
    python manage.py create_sample_data
    ```
4.  **Fire it up:**
    ```bash
    python manage.py runserver
    ```

You can then find the site at `http://127.0.0.1:8000/`. To get into the admin panel, use `admin` / `admin123`.

---

### A Bit About the Tech

We kept the stack pretty standard so it's easy to maintain:
- **Backend:** Django
- **UI:** Bootstrap 5 with a custom dark theme
- **Database:** SQLite (perfect for local dev)
- **Forms:** Crispy Forms for that clean look
- **Security:** Built-in Django auth with role-based permissions

---

### How it Works (The Workflow)

It's a pretty straightforward flow:
1.  **Organizers** create a contest and add links to the problems.
2.  **Participants** join the contest and upload their work (ZIP, link, image, etc.) before the timer hits zero.
3.  **Judges** review the submissions, download files if needed, and enter their scores.
4.  **The System** calculates the average score and updates the leaderboard in real-time.

---

Happy coding!
