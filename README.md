# Team Task Manager 🚀

Hey! Welcome to my Team Task Manager project. I built this full-stack application to help teams keep track of their ongoing projects and assign tasks efficiently. 

## What This App Does
I designed this to solve a common problem: keeping a team organized and on the same page. The app lets users sign up as either an `Admin` or a `Team Member`. 
- **Admins** have the authority to create new projects and assign tasks inside those projects.
- **Team Members** can view all available projects, assign unassigned tasks to themselves, and update their progress.

I went with a Kanban-style approach for the task board (To Do -> In Progress -> Done) because it's the most intuitive way to visualize workflow.

## Features I Implemented
* **Authentication:** Full signup/login system using `Flask-Login` and `Werkzeug` for secure password hashing.
* **Role-Based Access Control (RBAC):** Strict permissions depending on if you are an Admin or a Member.
* **Dashboard Analytics:** I went a bit beyond the basic requirements and added a dynamic doughnut chart using `Chart.js` so you can instantly see how many tasks are completed versus pending.
* **Activity Audit Log:** I thought it would be a realistic business feature to track what people are actually doing. So I created an `ActivityLog` model that records whenever someone creates a project, claims a task, or changes a status. It shows up as a live feed on the dashboard!
* **REST API Endpoint:** There's a `/api/tasks` endpoint that returns user task data in pure JSON.

## The Tech Stack
* **Backend:** Python and Flask. I chose Flask because it's lightweight and gives me a lot of control over the routing and application structure.
* **Database:** SQLite for local testing, which seamlessly swaps to PostgreSQL in production. I used `SQLAlchemy` as the ORM to manage the database relationships between Users, Projects, and Tasks. (I also specifically used the `pg8000` pure Python driver to avoid any library issues during deployment).
* **Frontend:** HTML templates with Jinja2. I decided to write pure Vanilla CSS from scratch instead of using a framework like Bootstrap. I wanted full control over the design to build a custom dark-mode "glass" UI effect.
* **Deployment:** Hosted live on Railway using `gunicorn` as the production web server.

## How to Run It Locally
If you want to run my code on your own machine, follow these steps:

1. Clone this repository to your computer.
2. Open your terminal in the project folder and install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your web browser and go to `http://127.0.0.1:5000`. You can create an Admin account first to set up some test projects!

## Links
* **Live Demo URL:** [Insert your Railway link here]
* **Demo Video:** [Insert your Video link here]
