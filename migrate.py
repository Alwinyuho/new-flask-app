from app import db, app
from app import User  # Import the User model
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create tables
    db.create_all()

    # Create an admin user (optional)
    hashed_password = generate_password_hash("Alwin@2469", method='pbkdf2:sha256')
    new_user = User(username="Alwinyuho", password=hashed_password)

    # Add to the database
    db.session.add(new_user)
    db.session.commit()

    print("✅ Database initialized and user created successfully!")
