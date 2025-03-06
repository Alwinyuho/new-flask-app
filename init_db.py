from app import db
from app import User  # Import your User model
from werkzeug.security import generate_password_hash

# Create the database tables if they don't exist
db.create_all()

# Hash the password
hashed_password = generate_password_hash("Alwin@2469", method='pbkdf2:sha256')

# Create a new user
new_user = User(username="Alwinyuho", password=hashed_password)

# Add the user to the database
db.session.add(new_user)
db.session.commit()

print("User 'Alwinyuho' has been created successfully!")
