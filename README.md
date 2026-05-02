# Team Task Manager

A full-stack web application designed for teams to manage projects, assign tasks, and track their overall progress. Built with Flask, SQLAlchemy, and a custom vanilla CSS glassmorphism UI.

## 🚀 Key Features
- **Role-Based Access Control:** Users are separated into `Admin` and `Member` roles.
- **Project & Team Management:** Admins create projects and assign tasks to members.
- **Task Tracking System:** Live Kanban-style tracking of task statuses (`To Do`, `In Progress`, `Done`).
- **Dashboard:** At-a-glance view of total projects, assigned tasks, overdue tasks, and a project completion progress tracker.
- **Dynamic Task Claiming:** Unassigned tasks can be claimed by team members using an "Assign to me" feature.
- **REST APIs:** Exposes an `/api/tasks` JSON endpoint.

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLAlchemy (SQLite for local dev, PostgreSQL for production)
- **Authentication:** Flask-Login, Werkzeug Security
- **Frontend:** HTML5, Jinja2 Templates, Vanilla CSS (Glassmorphism & Dark Mode)
- **Server:** Gunicorn (for production deployment)

## 🏃‍♂️ Running Locally

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone <your-repo-url>
   cd team-task-manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000`

## ☁️ Deployment (Railway)

This application is configured for easy deployment on [Railway.app](https://railway.app/).

1. Create a GitHub repository and push this code.
2. Log into Railway and click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Add a **PostgreSQL** Database to your Railway project.
5. In your Railway Web service settings, go to the **Variables** tab and add the following:
   - `DATABASE_URL` = (Reference the PostgreSQL database URL provided by Railway)
   - `SECRET_KEY` = (A random, secure string for Flask sessions)
6. Railway will automatically detect the `Procfile` and deploy the app!

## 🎥 Demo Video
*(Link your 2-5 minute demo video here)*
