from app import app, db, User
from werkzeug.security import generate_password_hash
import os
import getpass

with app.app_context():
    # Create admin user, password provided by env var DEFAULT_ADMIN_PASSWORD or prompted interactively
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        pwd = os.environ.get('DEFAULT_ADMIN_PASSWORD')
        if not pwd:
            # Ask for a password in interactive shells (hidden)
            try:
                pwd = getpass.getpass('Enter password for new admin user: ')
            except Exception:
                print('No DEFAULT_ADMIN_PASSWORD in environment and cannot prompt for password. Aborting.')
                raise SystemExit(1)

        admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash(pwd), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created with username: admin')
    else:
        print('Admin user already exists')
