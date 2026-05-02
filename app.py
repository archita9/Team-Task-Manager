from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key-for-dev')

db_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Member') # Admin or Member
    
    tasks_assigned = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee', lazy=True)
    projects_created = db.relationship('Project', backref='creator', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    tasks = db.relationship('Task', backref='project', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), nullable=False, default='To Do') # To Do, In Progress, Done
    due_date = db.Column(db.Date, nullable=True)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='activities', lazy=True)

def log_activity(user_id, action):
    log = ActivityLog(user_id=user_id, action=action)
    db.session.add(log)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'Member')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'error')
            return redirect(url_for('signup'))

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username and password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    projects = Project.query.all()
    
    if current_user.role == 'Admin':
        tasks = Task.query.all()
    else:
        tasks = current_user.tasks_assigned
    
    overdue_tasks = [t for t in tasks if t.due_date and t.due_date < today and t.status != 'Done']
    to_do = [t for t in tasks if t.status == 'To Do']
    in_progress = [t for t in tasks if t.status == 'In Progress']
    done = [t for t in tasks if t.status == 'Done']

    recent_activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(8).all()

    return render_template('dashboard.html', 
        projects=projects, 
        tasks=tasks, 
        overdue_tasks=overdue_tasks,
        to_do=to_do, in_progress=in_progress, done=done,
        recent_activities=recent_activities
    )

@app.route('/project/create', methods=['POST'])
@login_required
def create_project():
    if current_user.role != 'Admin':
        flash('Only Admins can create projects.', 'error')
        return redirect(url_for('dashboard'))
        
    name = request.form.get('name')
    description = request.form.get('description')
    if name:
        new_project = Project(name=name, description=description, created_by=current_user.id)
        db.session.add(new_project)
        log_activity(current_user.id, f"Created new project: {name}")
        db.session.commit()
        flash('Project created successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/project/<int:project_id>')
@login_required
def project_details(project_id):
    project = Project.query.get_or_404(project_id)
    users = User.query.all()
    return render_template('project.html', project=project, users=users)

@app.route('/task/create/<int:project_id>', methods=['POST'])
@login_required
def create_task(project_id):
    if current_user.role != 'Admin':
        flash('Only Admins can create tasks.', 'error')
        return redirect(url_for('project_details', project_id=project_id))
        
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    assigned_to = request.form.get('assigned_to')
    
    due_date = None
    if due_date_str:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
    if title:
        new_task = Task(
            title=title, 
            description=description, 
            due_date=due_date,
            project_id=project_id,
            assigned_to=assigned_to if assigned_to else None,
            created_by=current_user.id
        )
        db.session.add(new_task)
        log_activity(current_user.id, f"Created task '{title}'")
        db.session.commit()
        flash('Task created successfully.', 'success')
    return redirect(url_for('project_details', project_id=project_id))

@app.route('/task/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role != 'Admin' and task.assigned_to != current_user.id:
        flash('You do not have permission to update this task.', 'error')
        return redirect(url_for('dashboard'))
        
    status = request.form.get('status')
    if status in ['To Do', 'In Progress', 'Done']:
        task.status = status
        log_activity(current_user.id, f"Moved task '{task.title}' to {status}")
        db.session.commit()
        flash('Task status updated.', 'success')
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/task/assign_to_me/<int:task_id>', methods=['POST'])
@login_required
def assign_to_me(task_id):
    task = Task.query.get_or_404(task_id)
    if not task.assigned_to:
        task.assigned_to = current_user.id
        log_activity(current_user.id, f"Claimed task '{task.title}'")
        db.session.commit()
        flash('Task assigned to you successfully.', 'success')
    return redirect(request.referrer or url_for('dashboard'))

# --- API Endpoints ---
@app.route('/api/tasks', methods=['GET'])
@login_required
def api_tasks():
    if current_user.role == 'Admin':
        tasks = Task.query.all()
    else:
        tasks = current_user.tasks_assigned
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'status': t.status,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'project_id': t.project_id
    } for t in tasks])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
