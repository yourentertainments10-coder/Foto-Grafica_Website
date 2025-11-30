from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create admin user
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('admin123'), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with username: admin, password: admin123")
    else:
        print("Admin user already exists")
