from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, BooleanField, FileField, FieldList, FormField
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable debug mode and detailed error logging
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# Add custom Jinja filter for from_json
app.jinja_env.filters['from_json'] = json.loads

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Add sample data if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            email='admin@fotografica.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
    
    if not AboutContent.query.first():
        about_content = AboutContent(
            title='Our Mission',
            content='To foster creativity and excellence in photography and design by providing a platform for learning, collaboration, and artistic expression. We aim to capture life\'s most beautiful moments while building a supportive community of creative individuals who inspire each other to reach new heights.'
        )
        db.session.add(about_content)
    
    if not Event.query.first():
        sample_event = Event(
            title='Photography Workshop',
            description='Join us for an exciting photography workshop where you can learn new techniques and improve your skills.',
            date=datetime(2024, 12, 15),
            location='Community Center',
            image_path='https://images.unsplash.com/photo-1554048612-b6a1b612b786?w=400&h=250&fit=crop'
        )
        db.session.add(sample_event)
    
    if not GalleryItem.query.first():
        sample_gallery = GalleryItem(
            title='Sunset Portrait',
            description='A beautiful sunset portrait captured during our last event.',
            image_path='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
            category='portrait'
        )
        db.session.add(sample_gallery)
    
    if not HomeContent.query.first():
        home_content = HomeContent(
            hero_subtitle="Capturing moments, creating memories, and fostering creative talent through photography, design, and creative media.",
            features='[{"title": "Photography Excellence", "description": "Capturing life\'s most beautiful moments with artistic vision and technical precision."}, {"title": "Creative Community", "description": "A diverse team of passionate photographers and creative media enthusiasts."}, {"title": "Exciting Events", "description": "Regular workshops, competitions, and collaborative projects to enhance skills."}, {"title": "Recognition & Growth", "description": "Showcasing talent and providing opportunities for creative development."}]',
            cta_text="Discover amazing events, connect with talented individuals, and showcase your creative work."
        )
        db.session.add(home_content)
    
    if not TeamMember.query.filter_by(is_core=True).first():
        core_members = [
            TeamMember(name='Alex Rodriguez', role='Club President', specialty='Portrait & Event Photography', bio='Leading the club with 5+ years of photography experience. Specializes in capturing emotions and storytelling through portraits.', achievements='["Best Portrait 2024", "Event Photographer of the Year"]', image='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/alex", "email": "alex@fotografica.com"}', is_core=True),
            TeamMember(name='Maya Chen', role='Creative Director', specialty='Digital Art & Design', bio='Passionate about blending photography with digital art. Creates stunning visual compositions and manages our creative projects.', achievements='["Digital Artist Award 2024", "Creative Innovation Prize"]', image='https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/maya", "email": "maya@fotografica.com"}', is_core=True),
            TeamMember(name='James Wilson', role='Technical Lead', specialty='Equipment & Post-Processing', bio='Expert in camera equipment and advanced post-processing techniques. Conducts technical workshops and equipment training.', achievements='["Technical Excellence Award", "Workshop Leader 2024"]', image='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/james", "email": "james@fotografica.com"}', is_core=True),
            TeamMember(name='Sofia Martinez', role='Events Coordinator', specialty='Event Management & Documentation', bio='Organizes all club events and ensures seamless execution. Expert in event photography and community building.', achievements='["Event Excellence Award", "Community Builder 2024"]', image='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/sofia", "email": "sofia@fotografica.com"}', is_core=True)
        ]
        for member in core_members:
            db.session.add(member)
    
    if not TeamMember.query.filter_by(is_core=False).first():
        active_members = [
            TeamMember(name='David Kim', role='Senior Member', specialty='Landscape Photography', bio='Passionate landscape photographer capturing nature\'s beauty.', achievements='[]', image='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/david", "email": "david@fotografica.com"}', is_core=False),
            TeamMember(name='Emma Thompson', role='Senior Member', specialty='Fashion Photography', bio='Specializes in fashion and portrait photography.', achievements='[]', image='https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/emma", "email": "emma@fotografica.com"}', is_core=False),
            TeamMember(name='Ryan Patel', role='Active Member', specialty='Street Photography', bio='Capturing urban life and candid moments.', achievements='[]', image='https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/ryan", "email": "ryan@fotografica.com"}', is_core=False),
            TeamMember(name='Lisa Zhang', role='Active Member', specialty='Macro Photography', bio='Exploring the tiny details in nature and everyday objects.', achievements='[]', image='https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/lisa", "email": "lisa@fotografica.com"}', is_core=False),
            TeamMember(name='Michael Brown', role='Active Member', specialty='Documentary Photography', bio='Telling stories through visual narratives.', achievements='[]', image='https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/michael", "email": "michael@fotografica.com"}', is_core=False),
            TeamMember(name='Aria Johnson', role='Active Member', specialty='Abstract Art', bio='Creating artistic interpretations through photography.', achievements='[]', image='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/aria", "email": "aria@fotografica.com"}', is_core=False)
        ]
        for member in active_members:
            db.session.add(member)
    
    if not ContactInfo.query.first():
        contact_info = ContactInfo(
            email='foto.grafica@example.com',
            phone='+1 (555) 123-4567',
            phone_hours='Mon-Fri, 9AM-6PM PST',
            address='{"line1": "Creative Arts Center", "line2": "123 Photography Lane", "city": "San Francisco", "state": "CA", "zip": "94102"}',
            office_hours='{"weekdays": "Monday - Friday: 9:00 AM - 6:00 PM", "weekend": "Saturday: 10:00 AM - 4:00 PM", "closed": "Sunday: Closed"}',
            social_links='{"instagram": "https://instagram.com/fotografica", "facebook": "https://facebook.com/fotografica", "twitter": "https://twitter.com/fotografica", "instagram_handle": "@fotografica"}',
            faq='[{"question": "How can I join the club?", "answer": "Simply contact us through the form or email. We welcome photographers of all skill levels!"}, {"question": "Do you offer photography services?", "answer": "Yes! We provide professional photography services for events, portraits, and commercial projects."}, {"question": "What equipment do I need?", "answer": "Any camera works! We focus on creativity and technique rather than expensive equipment."}]'
        )
        db.session.add(contact_info)
    
    db.session.commit()

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    image_path = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='all')
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class HomeContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_subtitle = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text, nullable=False)  # JSON string
    cta_text = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    achievements = db.Column(db.Text, nullable=False)  # JSON string
    image = db.Column(db.String(200), nullable=False)
    social = db.Column(db.Text, nullable=False)  # JSON string
    is_core = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    phone_hours = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)  # JSON string
    office_hours = db.Column(db.Text, nullable=False)  # JSON string
    social_links = db.Column(db.Text, nullable=False)  # JSON string
    faq = db.Column(db.Text, nullable=False)  # JSON string
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Subforms
class FeatureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class FAQForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class AboutForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    location = StringField('Location')
    image = FileField('Image')
    submit = SubmitField('Add Event')

class GalleryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    image_path = FileField('Image', validators=[DataRequired()])
    category = SelectField('Category', choices=[('all', 'All'), ('portrait', 'Portrait'), ('landscape', 'Landscape'), ('street', 'Street'), ('nature', 'Nature'), ('events', 'Events')])
    submit = SubmitField('Add Gallery Item')

class HomeForm(FlaskForm):
    hero_subtitle = TextAreaField('Hero Subtitle', validators=[DataRequired()])
    features = FieldList(FormField(FeatureForm), min_entries=1)
    cta_text = TextAreaField('CTA Text', validators=[DataRequired()])
    submit = SubmitField('Update Home')

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    role = StringField('Role', validators=[DataRequired(), Length(max=50)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    achievements = FieldList(StringField('Achievement'), min_entries=1)
    image = StringField('Image URL', validators=[DataRequired()])
    instagram = StringField('Instagram')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    email = StringField('Email')
    is_core = BooleanField('Core Team Member')
    submit = SubmitField('Save Team Member')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=50)])
    phone_hours = StringField('Phone Hours', validators=[DataRequired(), Length(max=100)])
    line1 = StringField('Address Line 1', validators=[DataRequired()])
    line2 = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    weekdays = StringField('Weekdays Hours', validators=[DataRequired()])
    weekend = StringField('Weekend Hours', validators=[DataRequired()])
    closed = StringField('Closed Days', validators=[DataRequired()])
    instagram = StringField('Instagram')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    instagram_handle = StringField('Instagram Handle')
    faq = FieldList(FormField(FAQForm), min_entries=1)
    submit = SubmitField('Update Contact')

@app.route('/')
def index():
    home_content = HomeContent.query.first()
    hero_subtitle = home_content.hero_subtitle if home_content else "Capturing moments, creating memories, and fostering creative talent through photography, design, and creative media."
    features_json = home_content.features if home_content else '[{"title": "Photography Excellence", "description": "Capturing life\'s most beautiful moments with artistic vision and technical precision."}, {"title": "Creative Community", "description": "A diverse team of passionate photographers and creative media enthusiasts."}, {"title": "Exciting Events", "description": "Regular workshops, competitions, and collaborative projects to enhance skills."}, {"title": "Recognition & Growth", "description": "Showcasing talent and providing opportunities for creative development."}]'
    features = json.loads(features_json)
    cta_text = home_content.cta_text if home_content else "Discover amazing events, connect with talented individuals, and showcase your creative work."
    return render_template('index.html', hero_subtitle=hero_subtitle, features=features, cta_text=cta_text)

@app.route('/about')
def about():
    content = AboutContent.query.first()
    return render_template('about.html', content=content)

@app.route('/events')
def events():
    from datetime import datetime
    events = Event.query.all()
    current_time = datetime.now()
    return render_template('events.html', events=events, current_time=current_time)

@app.route('/team')
def team():
    core_team = TeamMember.query.filter_by(is_core=True).all()
    active_members = TeamMember.query.filter_by(is_core=False).all()
    return render_template('team.html', core_team=core_team, active_members=active_members)

@app.route('/gallery')
def gallery():
    gallery_items = GalleryItem.query.all()
    return render_template('gallery.html', gallery_items=gallery_items)

@app.route('/contact')
def contact():
    contact_info = ContactInfo.query.first()
    if not contact_info:
        contact_info = ContactInfo(
            email='foto.grafica@example.com',
            phone='+1 (555) 123-4567',
            phone_hours='Mon-Fri, 9AM-6PM PST',
            address='{"line1": "Creative Arts Center", "line2": "123 Photography Lane", "city": "San Francisco", "state": "CA", "zip": "94102"}',
            office_hours='{"weekdays": "Monday - Friday: 9:00 AM - 6:00 PM", "weekend": "Saturday: 10:00 AM - 4:00 PM", "closed": "Sunday: Closed"}',
            social_links='{"instagram": "https://instagram.com/fotografica", "facebook": "https://facebook.com/fotografica", "twitter": "https://twitter.com/fotografica", "instagram_handle": "@fotografica"}',
            faq='[{"question": "How can I join the club?", "answer": "Simply contact us through the form or email. We welcome photographers of all skill levels!"}, {"question": "Do you offer photography services?", "answer": "Yes! We provide professional photography services for events, portraits, and commercial projects."}, {"question": "What equipment do I need?", "answer": "Any camera works! We focus on creativity and technique rather than expensive equipment."}]'
        )
    return render_template('contact.html', contact_info=contact_info)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ResetForm()
    if form.validate_on_submit():
        if form.username.data == 'admin':
            user = User.query.filter_by(username='admin').first()
            if user:
                user.password = generate_password_hash('admin123')
                db.session.commit()
                flash('Password reset successfully! New password: admin123', 'success')
                return redirect(url_for('login'))
            else:
                flash('Admin user not found.', 'danger')
        else:
            flash('Only admin password can be reset.', 'danger')
    return render_template('forgot_password.html', form=form)

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/admin/home', methods=['GET', 'POST'])
@login_required
def manage_home():
    form = HomeForm()
    home_content = HomeContent.query.first()
    if form.validate_on_submit():
        if not home_content:
            home_content = HomeContent()
            db.session.add(home_content)
        home_content.hero_subtitle = form.hero_subtitle.data
        features_data = [{'title': f.title.data, 'description': f.description.data} for f in form.features]
        home_content.features = json.dumps(features_data)
        home_content.cta_text = form.cta_text.data
        db.session.commit()
        flash('Home content updated successfully!', 'success')
        return redirect(url_for('manage_home'))
    elif request.method == 'GET' and home_content:
        form.hero_subtitle.data = home_content.hero_subtitle
        features_list = json.loads(home_content.features)
        form.features.entries = [FeatureForm(title=f['title'], description=f['description']) for f in features_list]
        form.cta_text.data = home_content.cta_text
    features = json.loads(home_content.features) if home_content else []
    return render_template('manage_home.html', form=form, home_content=home_content, features=features)

@app.route('/admin/about', methods=['GET', 'POST'])
@login_required
def manage_about():
    form = AboutForm()
    content = AboutContent.query.first()
    if form.validate_on_submit():
        if not content:
            content = AboutContent()
            db.session.add(content)
        content.title = form.title.data
        content.content = form.content.data
        db.session.commit()
        flash('About content updated successfully!', 'success')
        return redirect(url_for('manage_about'))
    elif request.method == 'GET' and content:
        form.title.data = content.title
        form.content.data = content.content
    return render_template('manage_about.html', form=form, content=content)

@app.route('/admin/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=datetime.strptime(form.date.data, '%Y-%m-%d'),
            location=form.location.data
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(app.root_path, 'static', 'images', 'events', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.image.data.save(filepath)
            event.image_path = f'/static/images/events/{filename}'
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('manage_events'))
    events = Event.query.all()
    current_time = datetime.now()
    return render_template('manage_events.html', form=form, events=events, current_time=current_time)

@app.route('/admin/team', methods=['GET', 'POST'])
@login_required
def manage_team():
    form = TeamMemberForm()
    if form.validate_on_submit():
        achievements_data = [a.data for a in form.achievements if a.data]
        social_data = {'instagram': form.instagram.data, 'facebook': form.facebook.data, 'twitter': form.twitter.data, 'email': form.email.data}
        member = TeamMember(
            name=form.name.data,
            role=form.role.data,
            specialty=form.specialty.data,
            bio=form.bio.data,
            achievements=json.dumps(achievements_data),
            image=form.image.data,
            social=json.dumps(social_data),
            is_core=form.is_core.data
        )
        db.session.add(member)
        db.session.commit()
        flash('Team member added successfully!', 'success')
        return redirect(url_for('manage_team'))
    core_team = TeamMember.query.filter_by(is_core=True).all()
    active_members = TeamMember.query.filter_by(is_core=False).all()
    return render_template('manage_team.html', form=form, core_team=core_team, active_members=active_members)

@app.route('/admin/team/edit/<int:member_id>', methods=['GET', 'POST'])
@login_required
def edit_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)
    form = TeamMemberForm()
    if form.validate_on_submit():
        achievements_data = [a.data for a in form.achievements if a.data]
        social_data = {'instagram': form.instagram.data, 'facebook': form.facebook.data, 'twitter': form.twitter.data, 'email': form.email.data}
        member.name = form.name.data
        member.role = form.role.data
        member.specialty = form.specialty.data
        member.bio = form.bio.data
        member.achievements = json.dumps(achievements_data)
        member.image = form.image.data
        member.social = json.dumps(social_data)
        member.is_core = form.is_core.data
        db.session.commit()
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('manage_team'))
    elif request.method == 'GET':
        form.name.data = member.name
        form.role.data = member.role
        form.specialty.data = member.specialty
        form.bio.data = member.bio
        achievements_list = json.loads(member.achievements)
        form.achievements.entries = [StringField('Achievement', default=a) for a in achievements_list]
        form.image.data = member.image
        social_dict = json.loads(member.social)
        form.instagram.data = social_dict.get('instagram', '')
        form.facebook.data = social_dict.get('facebook', '')
        form.twitter.data = social_dict.get('twitter', '')
        form.email.data = social_dict.get('email', '')
        form.is_core.data = member.is_core
    return render_template('edit_team_member.html', form=form, member=member)

@app.route('/admin/team/delete/<int:member_id>')
@login_required
def delete_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Team member deleted successfully!', 'success')
    return redirect(url_for('manage_team'))

@app.route('/admin/contact', methods=['GET', 'POST'])
@login_required
def manage_contact():
    form = ContactForm()
    contact_info = ContactInfo.query.first()
    if form.validate_on_submit():
        if not contact_info:
            contact_info = ContactInfo()
            db.session.add(contact_info)
        contact_info.email = form.email.data
        contact_info.phone = form.phone.data
        contact_info.phone_hours = form.phone_hours.data
        address_data = {'line1': form.line1.data, 'line2': form.line2.data or '', 'city': form.city.data, 'state': form.state.data, 'zip': form.zip_code.data}
        contact_info.address = json.dumps(address_data)
        office_hours_data = {'weekdays': form.weekdays.data, 'weekend': form.weekend.data, 'closed': form.closed.data}
        contact_info.office_hours = json.dumps(office_hours_data)
        social_links_data = {'instagram': form.instagram.data or '', 'facebook': form.facebook.data or '', 'twitter': form.twitter.data or '', 'instagram_handle': form.instagram_handle.data or ''}
        contact_info.social_links = json.dumps(social_links_data)
        faq_data = [{'question': f.question.data, 'answer': f.answer.data} for f in form.faq.entries if f.question.data and f.answer.data]
        contact_info.faq = json.dumps(faq_data)
        db.session.commit()
        flash('Contact info updated successfully!', 'success')
        return redirect(url_for('manage_contact'))
    if request.method == 'GET' and contact_info:
        form.email.data = contact_info.email
        form.phone.data = contact_info.phone
        form.phone_hours.data = contact_info.phone_hours
        try:
            address_dict = json.loads(contact_info.address or '{}')
            form.line1.data = address_dict.get('line1', '')
            form.line2.data = address_dict.get('line2', '')
            form.city.data = address_dict.get('city', '')
            form.state.data = address_dict.get('state', '')
            form.zip_code.data = address_dict.get('zip', '')
        except:
            pass
        try:
            office_dict = json.loads(contact_info.office_hours or '{}')
            form.weekdays.data = office_dict.get('weekdays', '')
            form.weekend.data = office_dict.get('weekend', '')
            form.closed.data = office_dict.get('closed', '')
        except:
            pass
        try:
            social_dict = json.loads(contact_info.social_links or '{}')
            form.instagram.data = social_dict.get('instagram', '')
            form.facebook.data = social_dict.get('facebook', '')
            form.twitter.data = social_dict.get('twitter', '')
            form.instagram_handle.data = social_dict.get('instagram_handle', '')
        except:
            pass
        try:
            faq_list = json.loads(contact_info.faq or '[]')
            form.faq.entries = [FAQForm(question=f.get('question', ''), answer=f.get('answer', '')) for f in faq_list]
        except:
            form.faq.entries = []
    social = json.loads(contact_info.social_links) if contact_info and contact_info.social_links else {}
    faq = json.loads(contact_info.faq) if contact_info and contact_info.faq else []
    return render_template('manage_contact.html', form=form, contact_info=contact_info, social=social, faq=faq)

@app.route('/admin/gallery', methods=['GET', 'POST'])
@login_required
def manage_gallery():
    form = GalleryForm()
    if form.validate_on_submit():
        if form.image_path.data:
            filename = secure_filename(form.image_path.data.filename)
            filepath = os.path.join(app.root_path, 'static', 'images', filename)
            form.image_path.data.save(filepath)
            image_path = f'/static/images/{filename}'
        else:
            image_path = ''
        gallery_item = GalleryItem(
            title=form.title.data,
            description=form.description.data,
            image_path=image_path,
            category=form.category.data
        )
        db.session.add(gallery_item)
        db.session.commit()
        flash('Gallery item added successfully!', 'success')
        return redirect(url_for('manage_gallery'))
    gallery_items = GalleryItem.query.all()
    return render_template('manage_gallery.html', form=form, gallery_items=gallery_items)

@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = datetime.strptime(form.date.data, '%Y-%m-%d')
        event.location = form.location.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(app.root_path, 'static', 'images', 'events', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.image.data.save(filepath)
            event.image_path = f'/static/images/events/{filename}'
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('manage_events'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.date.data = event.date.strftime('%Y-%m-%d')
        form.location.data = event.location
    return render_template('edit_event.html', form=form, event=event)

@app.route('/admin/events/delete/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events'))

@app.route('/admin/gallery/edit/<int:gallery_id>', methods=['GET', 'POST'])
@login_required
def edit_gallery(gallery_id):
    gallery_item = GalleryItem.query.get_or_404(gallery_id)
    form = GalleryForm()
    if form.validate_on_submit():
        if form.image_path.data:
            filename = secure_filename(form.image_path.data.filename)
            filepath = os.path.join(app.root_path, 'static', 'images', filename)
            form.image_path.data.save(filepath)
            gallery_item.image_path = f'/static/images/{filename}'
        gallery_item.title = form.title.data
        gallery_item.description = form.description.data
        gallery_item.category = form.category.data
        db.session.commit()
        flash('Gallery item updated successfully!', 'success')
        return redirect(url_for('gallery'))
    elif request.method == 'GET':
        form.title.data = gallery_item.title
        form.description.data = gallery_item.description
        form.category.data = gallery_item.category
    return render_template('edit_gallery.html', form=form, gallery_item=gallery_item)

@app.route('/admin/gallery/delete/<int:gallery_id>')
@login_required
def delete_gallery(gallery_id):
    gallery_item = GalleryItem.query.get_or_404(gallery_id)
    db.session.delete(gallery_item)
    db.session.commit()
    flash('Gallery item deleted successfully!', 'success')
    return redirect(url_for('gallery'))

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Add sample data if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@fotografica.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
        
        if not AboutContent.query.first():
            about_content = AboutContent(
                title='Our Mission',
                content='To foster creativity and excellence in photography and design by providing a platform for learning, collaboration, and artistic expression. We aim to capture life\'s most beautiful moments while building a supportive community of creative individuals who inspire each other to reach new heights.'
            )
            db.session.add(about_content)
        
        if not Event.query.first():
            sample_event = Event(
                title='Photography Workshop',
                description='Join us for an exciting photography workshop where you can learn new techniques and improve your skills.',
                date=datetime(2024, 12, 15),
                location='Community Center',
                image_path='https://images.unsplash.com/photo-1554048612-b6a1b612b786?w=400&h=250&fit=crop'
            )
            db.session.add(sample_event)
        
        if not GalleryItem.query.first():
            sample_gallery = GalleryItem(
                title='Sunset Portrait',
                description='A beautiful sunset portrait captured during our last event.',
                image_path='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
                category='portrait'
            )
            db.session.add(sample_gallery)
        
        if not HomeContent.query.first():
            home_content = HomeContent(
                hero_subtitle="Capturing moments, creating memories, and fostering creative talent through photography, design, and creative media.",
                features='[{"title": "Photography Excellence", "description": "Capturing life\'s most beautiful moments with artistic vision and technical precision."}, {"title": "Creative Community", "description": "A diverse team of passionate photographers and creative media enthusiasts."}, {"title": "Exciting Events", "description": "Regular workshops, competitions, and collaborative projects to enhance skills."}, {"title": "Recognition & Growth", "description": "Showcasing talent and providing opportunities for creative development."}]',
                cta_text="Discover amazing events, connect with talented individuals, and showcase your creative work."
            )
            db.session.add(home_content)
        
        if not TeamMember.query.filter_by(is_core=True).first():
            core_members = [
                TeamMember(name='Alex Rodriguez', role='Club President', specialty='Portrait & Event Photography', bio='Leading the club with 5+ years of photography experience. Specializes in capturing emotions and storytelling through portraits.', achievements='["Best Portrait 2024", "Event Photographer of the Year"]', image='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/alex", "email": "alex@fotografica.com"}', is_core=True),
                TeamMember(name='Maya Chen', role='Creative Director', specialty='Digital Art & Design', bio='Passionate about blending photography with digital art. Creates stunning visual compositions and manages our creative projects.', achievements='["Digital Artist Award 2024", "Creative Innovation Prize"]', image='https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/maya", "email": "maya@fotografica.com"}', is_core=True),
                TeamMember(name='James Wilson', role='Technical Lead', specialty='Equipment & Post-Processing', bio='Expert in camera equipment and advanced post-processing techniques. Conducts technical workshops and equipment training.', achievements='["Technical Excellence Award", "Workshop Leader 2024"]', image='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/james", "email": "james@fotografica.com"}', is_core=True),
                TeamMember(name='Sofia Martinez', role='Events Coordinator', specialty='Event Management & Documentation', bio='Organizes all club events and ensures seamless execution. Expert in event photography and community building.', achievements='["Event Excellence Award", "Community Builder 2024"]', image='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=300&h=300&fit=crop&crop=face', social='{"instagram": "https://instagram.com/sofia", "email": "sofia@fotografica.com"}', is_core=True)
            ]
            for member in core_members:
                db.session.add(member)
        
        if not TeamMember.query.filter_by(is_core=False).first():
            active_members = [
                TeamMember(name='David Kim', role='Senior Member', specialty='Landscape Photography', bio='Passionate landscape photographer capturing nature\'s beauty.', achievements='[]', image='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/david", "email": "david@fotografica.com"}', is_core=False),
                TeamMember(name='Emma Thompson', role='Senior Member', specialty='Fashion Photography', bio='Specializes in fashion and portrait photography.', achievements='[]', image='https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/emma", "email": "emma@fotografica.com"}', is_core=False),
                TeamMember(name='Ryan Patel', role='Active Member', specialty='Street Photography', bio='Capturing urban life and candid moments.', achievements='[]', image='https://images.unsplash.com/photo-1507591064344-4c6ce005b128?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/ryan", "email": "ryan@fotografica.com"}', is_core=False),
                TeamMember(name='Lisa Zhang', role='Active Member', specialty='Macro Photography', bio='Exploring the tiny details in nature and everyday objects.', achievements='[]', image='https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/lisa", "email": "lisa@fotografica.com"}', is_core=False),
                TeamMember(name='Michael Brown', role='Active Member', specialty='Documentary Photography', bio='Telling stories through visual narratives.', achievements='[]', image='https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/michael", "email": "michael@fotografica.com"}', is_core=False),
                TeamMember(name='Aria Johnson', role='Active Member', specialty='Abstract Art', bio='Creating artistic interpretations through photography.', achievements='[]', image='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&h=200&fit=crop&crop=face', social='{"instagram": "https://instagram.com/aria", "email": "aria@fotografica.com"}', is_core=False)
            ]
            for member in active_members:
                db.session.add(member)
        
        if not ContactInfo.query.first():
            contact_info = ContactInfo(
                email='foto.grafica@example.com',
                phone='+1 (555) 123-4567',
                phone_hours='Mon-Fri, 9AM-6PM PST',
                address='{"line1": "Creative Arts Center", "line2": "123 Photography Lane", "city": "San Francisco", "state": "CA", "zip": "94102"}',
                office_hours='{"weekdays": "Monday - Friday: 9:00 AM - 6:00 PM", "weekend": "Saturday: 10:00 AM - 4:00 PM", "closed": "Sunday: Closed"}',
                social_links='{"instagram": "https://instagram.com/fotografica", "facebook": "https://facebook.com/fotografica", "twitter": "https://twitter.com/fotografica", "instagram_handle": "@fotografica"}',
                faq='[{"question": "How can I join the club?", "answer": "Simply contact us through the form or email. We welcome photographers of all skill levels!"}, {"question": "Do you offer photography services?", "answer": "Yes! We provide professional photography services for events, portraits, and commercial projects."}, {"question": "What equipment do I need?", "answer": "Any camera works! We focus on creativity and technique rather than expensive equipment."}]'
            )
            db.session.add(contact_info)
        
        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
