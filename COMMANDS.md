# HackHub-Code: Essential Commands Reference

This guide provides a quick reference for the Git and Django commands used during the development of HACKHUB-CODE. Use these for your viva or during local development.

---

## 🔧 Django Project Management
These commands are used to manage the database and run the server locally.

### 1. Initial Setup / Migrations
Run these if you change the models or reset the database.
```bash
python manage.py migrate
```

### 2. Create Sample Data
Generate a professional set of users (Admin, Organizer, Participant, Judge) and contests.
```bash
python manage.py create_sample_data
```

### 3. Start Development Server
```bash
python manage.py runserver 8001
```

---

## 🛠️ Git & Version Control
Essential commands for collaborating on GitHub.

### 1. Pulling Latest Changes
Before starting any work, always pull the latest code from GitHub to avoid conflicts.
```bash
git pull origin main
```

### 2. Checking Repository Status
See what files you have changed or haven't committed yet.
```bash
git status
```

### 3. Committing and Pushing
Follow this workflow to save your changes to GitHub:
```bash
# 1. Stage your changes
git add .

# 2. Save your changes with a clear message
git commit -m "Your descriptive message here"

# 3. Upload to GitHub
git push origin main
```

### 4. Viewing Commit History
Check who did what and when.
```bash
git log --oneline --graph --all
```

---

## 🧹 Cleaning Up History (Advanced)
If you have multiple small/messy commits and want to combine them into one professional commit (Squashing):
```bash
# 1. Reset back to a specific stable commit (keeping your code changes)
# Replace [COMMIT_ID] with the ID of the last 'good' commit
git reset --soft [COMMIT_ID]

# 2. Create a new single clean commit
git commit -m "feat: your consolidated feature name"

# 3. Update GitHub (requires force-push)
git push --force origin main
```

---
*University of Windsor | COMP-8347 Internet Applications*
