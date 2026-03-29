# DJANGO ADMIN PANEL GUIDE

This document contains the credentials and instructions for managing the **HACKHUB-CODE** platform using the built-in Django admin interface.

---

## 🔐 Credentials

| URL | Username | Password |
|---|---|---|
| `http://127.0.0.1:8000/admin/` | **admin** | **admin123** |

---

## 🛠️ What can the Admin do?

The admin panel is the "God Mode" of the application. As an administrator, you have full control over the database:

### 1. User Management (`Accounts` section)
- **View All Users**: See every registered organizer, participant, and judge.
- **Change Roles**: Manually upgrade a participant to an organizer or judge.
- **Reset Passwords**: Manually override passwords if a user is locked out.
- **Permissions**: Grant "Staff status" to other users if they need admin access.

### 2. Contest Management (`Contests` section)
- **Emergency Edits**: Modify contest details even after they have been published.
- **Problem Links**: Add or remove LeetCode/HackerRank links directly.
- **Status Control**: Manually toggle `is_published` or adjust `start_time` and `end_time` to fix scheduling errors.

### 3. Submission Monitoring (`Submissions` section)
- **View All Work**: See every file and link submitted by participants across all contests.
- **Audit**: Verify when a submission was made and check for potential duplicate work.

### 4. Score Overrides (`Scoring` section)
- **Review Scores**: See all judge evaluations and feedback.
- **Correction**: Edit or delete unfair or incorrect scores given by judges.

---

## 🚦 Important Notes for Demonstrations
- Avoid deleting the `admin` user, as it is required to manage the system.
- If you change a user's role in the admin panel, they must **log out and log back in** for the changes to take effect in their session.
- The admin panel uses the same custom user model defined in `accounts/models.py`.

---
*HACKHUB-CODE Admin Documentation - 2026*
