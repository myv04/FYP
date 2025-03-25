from app import app, db, bcrypt
from models import User

with app.app_context():
    db.drop_all()  # Deletes old database
    db.create_all()

    users = [
        User(username="student1", password=bcrypt.generate_password_hash("studentpass").decode('utf-8'), role="student"),
        User(username="lecturer1", password=bcrypt.generate_password_hash("lecturerpass").decode('utf-8'), role="lecturer"),
        User(username="admin1", password=bcrypt.generate_password_hash("adminpass").decode('utf-8'), role="admin"),
    ]

    db.session.add_all(users)
    db.session.commit()

    print("Database initialized with predefined users!")
