from app import db, app  # Import db and app correctly
from app import User  # Import User model
from werkzeug.security import generate_password_hash

# Ensure the app context is active
with app.app_context():
    # Create database tables if they don't exist
    db.create_all()

    # Check if user already exists to prevent duplicate entries
    if not User.query.filter_by(username="Alwinyuho").first():
        # Hash the password
        hashed_password = generate_password_hash("Alwin@2469", method='pbkdf2:sha256')

        # Create a new user
        new_user = User(username="Alwinyuho", password=hashed_password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        print("User 'Alwinyuho' has been created successfully!")
    else:
        print("User 'Alwinyuho' already exists!")
